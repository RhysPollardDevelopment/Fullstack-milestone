from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

import stripe


def not_subscribed(user):
    if user.is_authenticated:
        if user.userprofile.has_active_subscription:
            return False
        else:
            return True
    else:
        return True


@user_passes_test(not_subscribed, login_url="/", redirect_field_name=None)
def subscription_page(request):

    if request.user.is_authenticated:
        if request.user.userprofile.has_active_subscription:
            return redirect(reverse("home"))

    template = "subscriptions/subscriptions_page.html"
    # This relates to the djstripe product object which is the subscription
    # plan made on the Stripe dashboard.
    stripe.api_key = settings.STRIPE_SECRET_KEY
    products = stripe.Product.list()

    context = {
        "products": products,
    }
    return render(request, template, context)
