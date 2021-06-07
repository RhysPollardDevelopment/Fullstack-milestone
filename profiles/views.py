from profiles.forms import UserProfileForm
from django.utils import timezone
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile

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
        )

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

    template = "profiles/subscription_history.html"
    context = {
        "profile": profile,
    }
    return render(request, template, context)
