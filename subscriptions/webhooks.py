import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from profiles.models import UserProfile

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
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the
        # status in your
        # database to reference when a user accesses your service to
        # avoid hitting rate
        # limits.
        print("invoice paid")

        # When invoice is being created using this, check pre-made rewards
        # for their dates and assign correct one.

    if event_type == "invoice.payment_failed":
        # If the payment fails or the customer does not have a valid payment
        #  method,
        # an invoice.payment_failed event is sent, the subscription becomes
        #  past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        # print(data)
        print("invoice.payment_failed")

    if event_type == "customer.subscription.deleted":
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        # print(data)

        # Change this to set end date on individual subscription to now.
        print("customer.subscription.deleted")

    if event_type == "customer.subscription.created":
        # set up email to tell customer they have a new subscription.
        print("Subscription created")

    if event_type == "customer.subscription.updated":
        # set up email to tell customer they have a new subscription.
        print("Subscription updated")

    return JsonResponse({"status": "success"})
