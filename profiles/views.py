from profiles.forms import UserProfileForm
from django.utils import timezone
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from recipes.models import Recipe

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
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated Address")
            return redirect(reverse("profiles"))
        else:
            messages.error(
                request, "Update failed. Please check form for any errors."
            )
    else:
        form = UserProfileForm(instance=profile)
    template = "profiles/update_address.html"
    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, template, context)


@login_required
def password_change_done(request):
    template = "allauth/account/password_change_done.html"
    return render(request, template)


@login_required
def my_recipes(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    # Needs system to check if has recipes to show, if not then must be
    # redirected back to user profile.

    template = "profiles/my_recipes.html"
    context = {
        "profile": profile,
    }
    return render(request, template, context)


@login_required
def subscription_history(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    # Collects list of all profiles subscription models.
    stripe_sub = list(profile.stripesubscription_set.all())

    recipes_list = Recipe.objects.all()

    invoices = []

    # For each subscription in the list, it checks runs through every invoice.
    for sub in stripe_sub:
        sub_invoices = list(sub.invoice_set.all())

        # Each invoice checks if a recipe publish date falls between the
        # start and end of the invoice period.
        for sub_invoice in sub_invoices:
            for recipe in recipes_list:
                d = recipe.publish_date
                # If so then this is what customer received access to and is
                # added as part of the invoice list.
                if (
                    sub_invoice.current_start < d
                    and sub_invoice.current_end > d
                ):
                    sub_invoice.recipe = recipe
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
