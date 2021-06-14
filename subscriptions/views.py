from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone

# Forms and models imported.
from .forms import SubscriptionForm, BillingAddressForm
from profiles.models import UserProfile
from profiles.forms import UserProfileForm

import stripe
import json


def not_subscribed(user):
    """
    To prevent access to pages where subscribed users don't need to be.

    Checks if user has an active subscription, if so then redirects to prevent
    creation of multiple subscriptions at one time.
    """
    if user.is_authenticated:
        if user.userprofile.has_active_subscription:
            return False
        else:
            return True
    else:
        return True


# https://docs.djangoproject.com/en/1.10/topics/auth/default/#django
# .contrib.auth.decorators.user_passes_test - Found here on django docs.


@user_passes_test(not_subscribed, login_url="/", redirect_field_name=None)
def subscription_page(request):
    """Loads page containing details of subscription services and benefits"""

    template = "subscriptions/subscriptions_page.html"
    # This relates to the djstripe product object which is the subscription
    # plan made on the Stripe dashboard.
    stripe.api_key = settings.STRIPE_SECRET_KEY
    products = stripe.Product.list()

    context = {
        "products": products,
    }
    return render(request, template, context)


@user_passes_test(not_subscribed, login_url="/", redirect_field_name=None)
@login_required
def checkout(request):
    """
    Loads checkout page along with the subscription and billing forms.
    Prefills forms with any available information from models or stripe.
    """
    stripe_price_ID = settings.STRIPE_PRICE_ID
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    try:
        profile = UserProfile.objects.get(user=request.user)
        customer_id = profile.stripe_customer_id
        sub_form = SubscriptionForm(
            initial={
                "full_name": profile.user.get_full_name(),
                "phone_number": profile.default_phone_number,
                "street_address1": profile.default_street_address1,
                "street_address2": profile.default_street_address2,
                "town_or_city": profile.default_town_or_city,
                "county": profile.default_county,
                "postcode": profile.default_postcode,
            }
        )

    except UserProfile.DoesNotExist:
        sub_form = SubscriptionForm()

    # Data for billing form is loaded from Stripe as they handle payments
    # and is not essential to other areas of site.
    try:
        billing = stripe.Customer.retrieve(customer_id)
        if billing.address is not None:
            bill_form = BillingAddressForm(
                initial={
                    "billing_full_name": billing.name,
                    "billing_phone_number": billing["phone"],
                    "billing_address1": billing.address["line1"],
                    "billing_address2": billing.address["line2"],
                    "billing_town_or_city": billing.address["city"],
                    "billing_county": billing.address["state"],
                    "billing_postcode": billing.address["postal_code"],
                }
            )
        else:
            bill_form = BillingAddressForm()
    except UserProfile.DoesNotExist:
        bill_form = BillingAddressForm()

    template = "subscriptions/checkout.html"
    context = {
        "stripe_price_ID": stripe_price_ID,
        "stripe_public_key": stripe_public_key,
        "profile": profile,
        "sub_form": sub_form,
        "bill_form": bill_form,
    }
    return render(request, template, context)


@user_passes_test(not_subscribed, login_url="/", redirect_field_name=None)
@login_required
def create_subscription(request):
    """
    Create a Stripe Customer and Subscription object and update the customer's
    strip account.

    Attaches card method to user and also modifies card details before
    creating subscription.
    """
    # parse request, extract details, and verify assumptions
    if request.method == "POST":

        data = json.loads(request.body)

        # Plan selected through front end ID incase multiple options are
        # available in future.
        priceId = data["priceId"]

        form = SubscriptionForm(data)
        if form.is_valid():

            profile = UserProfile.objects.get(user=request.user)
            customer_id = profile.stripe_customer_id

            stripe.api_key = settings.STRIPE_SECRET_KEY
            # Collects shipping data and assigns it to the session to pass to
            # the complete view.
            request.session["save_shipping"] = data["saveShipping"]
            request.session["shippingdata"] = {
                "default_phone_number": data["phone_number"],
                "default_street_address1": data["street_address1"],
                "default_street_address2": data["street_address2"],
                "default_town_or_city": data["town_or_city"],
                "default_county": data["county"],
                "default_postcode": data["postcode"],
            }

            # If sameBilling is true, set data to shipping info or billing
            # info if false.
            if data["sameBilling"]:
                phone = data["phone_number"]
                address = {
                    "city": data["town_or_city"],
                    "line1": data["street_address1"],
                    "line2": data["street_address2"],
                    "postal_code": data["postcode"],
                    "state": data["county"],
                    "country": "GB",
                }
            else:
                phone = data["billing_phone_number"]
                address = {
                    "city": data["billing_town_or_city"],
                    "line1": data["billing_address1"],
                    "line2": data["billing_address2"],
                    "postal_code": data["billing_postcode"],
                    "state": data["billing_county"],
                    "country": "GB",
                }

            # Once data is assigned, tries to modify the stripe customer info.
            try:
                stripe.Customer.modify(
                    customer_id,
                    address=address,
                    phone=phone,
                    shipping={
                        # Name is required, unsure how to do this.
                        "name": data["full_name"],
                        "address": {
                            "city": data["town_or_city"],
                            "line1": data["street_address1"],
                            "line2": data["street_address2"],
                            "postal_code": data["postcode"],
                            "state": data["county"],
                            "country": "GB",
                        },
                        "phone": data["phone_number"],
                    },
                    email=profile.user.email,
                )

                # Attach the payment method to the customer
                stripe.PaymentMethod.attach(
                    data["paymentMethodId"],
                    customer=data["customerId"],
                )
                # Set the default payment method on the customer
                stripe.Customer.modify(
                    data["customerId"],
                    invoice_settings={
                        "default_payment_method": data["paymentMethodId"],
                    },
                )
                # create subscription
                subscription = stripe.Subscription.create(
                    customer=data["customerId"],
                    items=[
                        {
                            "price": priceId,
                        },
                    ],
                    expand=["latest_invoice.payment_intent"],
                )

                # associate subscription with the user
                # request.user.userprofile.subscription_id = subscription.id
                # request.user.save()
                # returns the subscription object information for front end.
                return JsonResponse(subscription)

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=200)
        else:
            messages.error(
                request, "Update failed. Please check form for any errors."
            )
    else:
        return HttpResponse("Request method not allowed")


@user_passes_test(not_subscribed, login_url="/", redirect_field_name=None)
@login_required
def complete(request):
    """
    Page sent to on successful subscription creation/payment. Also updates user
    information if save_shipping variable is true.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    save_shipping = request.session["save_shipping"]
    # Checks the state of save_shipping in the session.
    # If equals True, updates userprofile delivery address.
    if save_shipping:
        shipping_data = request.session["shippingdata"]

        update_form = UserProfileForm(shipping_data, instance=profile)
        if update_form.is_valid():
            update_form.save()
        messages.success(request, "Delivery information updated!")
        # Remove shippingdata for safety reasons, found on
        # https://docs.djangoproject.com/en/3.2/topics/http/sessions/
        del request.session["shippingdata"]

    template = "subscriptions/complete.html"
    return render(request, template)


@login_required
def cancel_subscription(request):
    """
    Stripe request to change stop auto-renewal of subscription, updates
    attribute on active subscription model also.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    today = timezone.now()
    stripe_sub = profile.stripesubscription_set.filter(end_date__gte=today)[0]

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        stripe.Subscription.modify(
            stripe_sub.subscription_id, cancel_at_period_end=True
        )
        stripe_sub.cancel_at_end = True
        stripe_sub.save()
    except Exception as e:
        print(e)
        return JsonResponse({"error": (e.args[0])}, status=403)
    template = "subscriptions/cancel_confirmation.html"
    context = {
        "subscription": stripe_sub,
    }
    return render(request, template, context)


@login_required
def reactivate(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    today = timezone.now()
    stripe_sub = profile.stripesubscription_set.filter(end_date__gte=today)[0]

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        stripe.Subscription.modify(
            stripe_sub.subscription_id,
            cancel_at_period_end=False,
            proration_behavior="none",
        )
        stripe_sub.cancel_at_end = False
        stripe_sub.save()
    except Exception as e:
        return JsonResponse({"error": (e.args[0])}, status=403)
    template = "subscriptions/reactivate_confirmation.html"
    context = {
        "subscription": stripe_sub,
    }
    return render(request, template, context)
