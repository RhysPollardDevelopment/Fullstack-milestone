from django.utils import timezone
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile


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
        subscription = profile.subscription_set.filter(
            expiry_date__isnull=True
        )[0]
    # If no active subscription, checks if user is in end period of a cancelled
    # subscription. If not then subscription remains empty.
    elif profile.subscription_set.filter(expiry_date__gte=today):
        subscription = profile.subscription_set.filter(expiry_date__gte=today)[
            0
        ]

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
        # Need to add in form
        messages.success(request, "Successfully Updated Address")
        return redirect(reverse("profiles"))
    template = "profiles/update_address.html"
    context = {
        "profile": profile,
    }
    return render(request, template, context)


@login_required
def change_password(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    template = "profiles/change_password.html"
    context = {
        "profile": profile,
    }
    return render(request, template, context)


@login_required
def my_recipes(request):
    profile = get_object_or_404(UserProfile, user=request.user)

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
