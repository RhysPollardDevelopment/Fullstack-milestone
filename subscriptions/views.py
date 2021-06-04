from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import SubscriptionForm, BillingAddressForm
from profiles.models import UserProfile
from profiles.forms import UserProfileForm

import stripe


def not_subscribed(user):
    """
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


@login_required
def checkout(request):

    stripe_price_ID = settings.STRIPE_PRICE_ID
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


@login_required
def complete(request):

    template = "subscriptions/complete.html"
    return render(request, template)
