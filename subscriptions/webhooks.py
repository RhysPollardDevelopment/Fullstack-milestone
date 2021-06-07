from datetime import datetime
import json
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta

from profiles.models import UserProfile
from .models import StripeSubscription, Invoice

import stripe


@require_POST
@csrf_exempt
def webhook_received(request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # You can use webhooks to receive information about asynchronous payment
    # events.
    # For more about our webhook events check out
    # https://stripe.com/docs/webhooks.
    request_data = json.loads(request.body)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body
        #  and secret if webhook signing is configured.
        signature = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data,
                sig_header=signature,
                secret=webhook_secret,
            )
            data = event["data"]
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status
        #  of PaymentIntents.
        event_type = event["type"]
    else:
        data = request_data["data"]
        event_type = request_data["type"]

    data_object = data["object"]

    if event_type == "invoice.paid":
        """
        Used to store invoice information and assign monthly rewards to
        history.
        """

        # Checks for subscription.cycle to prevent updating user for generic
        # updates or creating new accounts. Prevents errors with missing model
        # instances, plus user can only cancel or renew their subscription.
        if data_object["billing_reason"] == "subscription_cycle":
            subscription = data_object["subscription"]
            active_subscription = UserProfile.objects.get(
                subscription_id=subscription
            )
            invoice_shipping = data_object["customer_shipping"]
            Invoice.objects.create(
                stripe_subscription=active_subscription,
                invoice_number=data_object["id"],
                current_start=datetime.fromtimestamp(
                    data_object["current_period_start"], tz=timezone.utc
                ),
                current_end=datetime.fromtimestamp(
                    data_object["current_period_end"], tz=timezone.utc
                ),
                delivery_name=invoice_shipping["name"],
                address_1=invoice_shipping["address"]["line1"],
                address_2=invoice_shipping["address"]["line2"],
                town_or_city=invoice_shipping["address"]["city"],
                county=invoice_shipping["address"]["state"],
                postcode=invoice_shipping["address"]["postal_code"],
            )
            active_subscription.end_date = (
                datetime.fromtimestamp(
                    data_object["current_period_end"], tz=timezone.utc
                ),
            )
            active_subscription.save()

    if event_type == "invoice.payment_failed":
        # If the payment fails or the customer does not have a valid payment
        #  method,
        # an invoice.payment_failed event is sent, the subscription becomes
        #  past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        print("invoice.payment_failed")

    if event_type == "customer.subscription.deleted":
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        # print(data)

        # Use to send customer an email informing them and change subscription
        print("customer.subscription.deleted")

    if event_type == "customer.subscription.created":
        """
        Creats new instance of stripesubscription on subscriptions creation
        and assigns new invoice to this subscription.

        "Invoice.paid" may not be delivered first and would be invalid as no
        subscription would exist in model.
        """
        # set up email to tell customer they have a new subscription.
        # Find customer using stripe ID.
        customer_id = data_object["customer"]
        freebees_customer = UserProfile.objects.get(
            stripe_customer_id=customer_id
        )
        # Create and fill in new stripe subscription using stripe info and
        # customer from database.
        new_subscription = StripeSubscription.objects.create(
            subscription_id=data_object["id"],
            start_date=datetime.fromtimestamp(
                data_object["start_date"], tz=timezone.utc
            ),
            end_date=datetime.fromtimestamp(
                data_object["current_period_end"], tz=timezone.utc
            ),
            stripe_user=freebees_customer,
        )

        # Create new invoice instance using stripe data. Created here as
        # invoice.paid could come before subscription.created.
        # If so then no stripesubscription to assign to, causes error.
        first_invoice = stripe.Invoice.retrieve(data_object["latest_invoice"])
        invoice_shipping = data_object["latest_invoice"]["customer_shipping"]
        Invoice.objects.create(
            stripe_subscription=new_subscription,
            invoice_number=first_invoice["id"],
            current_start=datetime.fromtimestamp(
                data_object["current_period_start"], tz=timezone.utc
            ),
            current_end=datetime.fromtimestamp(
                data_object["current_period_end"], tz=timezone.utc
            ),
            delivery_name=invoice_shipping["name"],
            address_1=invoice_shipping["address"]["line1"],
            address_2=invoice_shipping["address"]["line2"],
            town_or_city=invoice_shipping["address"]["city"],
            county=invoice_shipping["address"]["state"],
            postcode=invoice_shipping["address"]["postal_code"],
        )

    if event_type == "customer.subscription.updated":
        # set up email to tell customer they have a new subscription.
        print("Subscription updated")
        print(data_object)

    return JsonResponse({"status": "success"})

    # customer.subscription.trial_will_end -

    # past_due - email customer about fact it has failed?
