from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required

# Forms and models imported.
from .forms import SubscriptionForm, BillingAddressForm
from profiles.models import UserProfile
from profiles.forms import UserProfileForm

import stripe
import json


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
def create_subscription(request):
    """
    Create a Stripe Customer and Subscription object and map them onto the User
    object.Expects the inbound POST data to look something like this:

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

            request.session["save_shipping"] = data["saveShipping"]
            request.session["shippingdata"] = {
                "default_phone_number": data["phone_number"],
                "default_street_address1": data["street_address1"],
                "default_street_address2": data["street_address2"],
                "default_town_or_city": data["town_or_city"],
                "default_county": data["county"],
                "default_postcode": data["postcode"],
            }

            # set data to shipping info or billing info if checkbox checked.
            if data["sameBilling"]:
                print("same")
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
                print("different")
                phone = data["billing_phone_number"]

                address = {
                    "city": data["billing_town_or_city"],
                    "line1": data["billing_address1"],
                    "line2": data["billing_address2"],
                    "postal_code": data["billing_postcode"],
                    "state": data["billing_county"],
                    "country": "GB",
                }
            print(address)

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
                request.user.userprofile.subscription_id = subscription.id
                request.user.save()

                return JsonResponse(subscription)

            except Exception as e:
                print("error")
                return JsonResponse({"error": str(e)}, status=200)
        else:
            messages.error(
                request, "Update failed. Please check form for any errors."
            )
    else:
        return HttpResponse("Request method not allowed")


@login_required
def complete(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    save_shipping = request.session["save_shipping"]

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
