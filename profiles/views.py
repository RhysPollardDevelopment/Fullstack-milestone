from profiles.forms import UserProfileForm
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
import stripe


from .models import UserProfile
from subscriptions.forms import BillingAddressForm

from allauth.account.views import PasswordChangeView


# Overload for success_url suggested in django documents but final solution:
# https://www.gitmemory.com/issue/pennersr/django-allauth/468/502080086
class CustomPasswordChangeView(PasswordChangeView):
    """
    Custom class overloads the success url method of all auth's password_change
    to correctly redirect to another page on form being valid.
    """

    success_url = "/accounts/password/change/done/"


@login_required
def profiles(request):
    """
    Directs logged in users to a profile page for their details and stored
    information.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    subscription = None
    today = timezone.now()

    # Checks is user has an active subscription.
    if profile.has_active_subscription:
        subscription = profile.stripesubscription_set.filter(
            end_date__gte=today
        )[0]

    template = "profiles/userprofile.html"
    context = {
        "subscription": subscription,
        "profile": profile,
    }
    return render(request, template, context)


@login_required
def update_address(request):
    """
    Updates customer delivery address locally and sends a copy to stripe.

    This is saved in database also as user is more likely to want to see
    their own delivery than billing information.
    """

    stripe.api_key = settings.STRIPE_SECRET_KEY

    profile = get_object_or_404(UserProfile, user=request.user)

    billing = stripe.Customer.retrieve(profile.stripe_customer_id)

    if billing.address:
        billing_info = {
            "billing_full_name": billing["name"],
            "billing_phone_number": billing["phone"],
            "billing_address1": billing.address["line1"],
            "billing_address2": billing.address["line2"],
            "billing_town_or_city": billing.address["city"],
            "billing_county": billing.address["state"],
            "billing_postcode": billing.address["postal_code"],
        }
    else:
        billing_info = {}

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            try:
                stripe.Customer.modify(
                    profile.stripe_customer_id,
                    shipping={
                        # Name is required, using old as same person.
                        "name": request.user.get_full_name(),
                        "address": {
                            "city": request.POST["default_town_or_city"],
                            "line1": request.POST["default_street_address1"],
                            "line2": request.POST["default_street_address2"],
                            "postal_code": request.POST["default_postcode"],
                            "state": request.POST["default_county"],
                            "country": "GB",
                        },
                        "phone": request.POST["default_phone_number"],
                    },
                    email=request.user.email,
                )
                form.save()
                messages.success(
                    request, "Successfully Updated delivery address."
                )
                return redirect(reverse("profiles"))
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=200)
        else:
            messages.error(
                request, "Update failed. Please check form for any errors."
            )
    else:
        form = UserProfileForm(instance=profile)

    bill_form = BillingAddressForm(initial=billing_info)
    template = "profiles/update_address.html"
    context = {
        "form": form,
        "profile": profile,
        "bill_form": bill_form,
    }
    return render(request, template, context)


@login_required
@require_POST
def update_billing(request):
    """
    Updates the billing address by sending customer modification to stripe.
    """

    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Collect user to find their stripe_id.
    profile = get_object_or_404(UserProfile, user=request.user)
    # Post only method.
    if request.method == "POST":

        bill_form = BillingAddressForm(request.POST)

        if bill_form.is_valid():
            try:
                # Attempt to modify customer billing address.
                stripe.Customer.modify(
                    profile.stripe_customer_id,
                    name=request.POST["billing_full_name"],
                    address={
                        "city": request.POST["billing_town_or_city"],
                        "line1": request.POST["billing_address1"],
                        "line2": request.POST["billing_address2"],
                        "postal_code": request.POST["billing_postcode"],
                        "state": request.POST["billing_county"],
                        "country": "GB",
                    },
                    phone=request.POST["billing_phone_number"],
                    email=request.user.email,
                )
                messages.success(
                    request, "Successfully Updated billing address"
                )
                return redirect(reverse("profiles"))
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=200)
        else:
            messages.error(
                request, "Update failed. Please check form for any errors."
            )
    else:
        return HttpResponse("Request method not allowed")


@login_required
def password_change_done(request):
    template = "allauth/account/password_change_done.html"
    return render(request, template)


@login_required
def subscription_history(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    # Collects list of all profiles subscription models.
    stripe_sub = list(profile.stripesubscription_set.all())

    invoices = []

    # For each subscription in the list, it checks runs through every invoice.
    for sub in stripe_sub:
        sub_invoices = sub.invoice_set.all()
        # Each invoice per sub is added to the invoices list.
        for sub_invoice in sub_invoices:
            invoices.append(sub_invoice)

    # https://www.w3schools.com/python/ref_list_sort.asp - ref for reverse.
    # https://wiki.python.org/moin/HowTo/Sorting#Sortingbykeys - using keys.
    invoices.sort(key=lambda x: x.current_start, reverse=True)

    template = "profiles/subscription_history.html"
    context = {
        "profile": profile,
        "invoices": invoices,
    }
    return render(request, template, context)
