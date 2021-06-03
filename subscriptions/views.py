from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.conf import settings

import stripe


def subscription_page(request):
    if request.user.userprofile.is_subscribed:
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
