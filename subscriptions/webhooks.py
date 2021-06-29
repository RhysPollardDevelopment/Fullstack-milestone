from datetime import datetime
import json
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.http import HttpResponse

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

        Also creates initial subscription incase authorisation fails, prevents
        incorrectly creating subscription by waiting for first invoice paid.
        """

        data = data_object["lines"]["data"]
        period = data[0]["period"]

        # If invoice paid is subscription_create, then this
        if data_object["billing_reason"] == "subscription_create":
            customer_id = data_object["customer"]
            freebees_customer = UserProfile.objects.get(
                stripe_customer_id=customer_id
            )

            # New variable as period["end"] was too short to break for pep8.
            end = period["end"]

            # Create and fill in new stripe subscription using stripe info and
            # customer from database invoice.
            new_subscription = StripeSubscription.objects.create(
                subscription_id=data_object["subscription"],
                start_date=datetime.fromtimestamp(
                    period["start"], tz=timezone.utc
                ),
                end_date=datetime.fromtimestamp(end, tz=timezone.utc),
                stripe_user=freebees_customer,
            )

            # Create new invoice instance using data from invoice.paid.
            # Assigns variables to invoice address and then sends email.
            invoice_shipping = data_object["customer_shipping"]
            invoice = Invoice.objects.create(
                stripe_subscription=new_subscription,
                invoice_number=data_object["id"],
                current_start=datetime.fromtimestamp(
                    period["start"], tz=timezone.utc
                ),
                current_end=datetime.fromtimestamp(
                    period["end"], tz=timezone.utc
                ),
                delivery_name=invoice_shipping["name"],
                address_1=invoice_shipping["address"]["line1"],
                address_2=invoice_shipping["address"]["line2"],
                town_or_city=invoice_shipping["address"]["city"],
                county=invoice_shipping["address"]["state"],
                postcode=invoice_shipping["address"]["postal_code"],
            )

            # Create email for customer.
            customer_email = freebees_customer.user.email
            # Subject template name shortened to conform PEP8
            subject = render_to_string(
                "subscriptions/email_templates/sub_created_subject.txt",
                {"invoice": invoice},
            )
            body = render_to_string(
                "subscriptions/email_templates/subscription_created_body.txt",
                {
                    "invoice": invoice,
                    "contact_email": settings.DEFAULT_FROM_EMAIL,
                },
            )
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [customer_email],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found")

        # Checks for subscription.cycle to prevent updating user for generic
        # updates or creating new accounts. Prevents errors with missing model
        # instances, plus user can only cancel or renew their subscription.
        if data_object["billing_reason"] == "subscription_cycle":
            subscription = data_object["subscription"]
            active_subscription = UserProfile.objects.get(
                subscription_id=subscription
            )
            invoice_shipping = data_object["customer_shipping"]

            # Assign values for address and start and end to database object.
            invoice = Invoice.objects.create(
                stripe_subscription=active_subscription,
                invoice_number=data_object["id"],
                current_start=datetime.fromtimestamp(
                    period["start"], tz=timezone.utc
                ),
                current_end=datetime.fromtimestamp(
                    period["end"], tz=timezone.utc
                ),
                delivery_name=invoice_shipping["name"],
                address_1=invoice_shipping["address"]["line1"],
                address_2=invoice_shipping["address"]["line2"],
                town_or_city=invoice_shipping["address"]["city"],
                county=invoice_shipping["address"]["state"],
                postcode=invoice_shipping["address"]["postal_code"],
            )

            # Updated subscription end-time to next billing end period.
            active_subscription.end_date = (
                datetime.fromtimestamp(period["end"], tz=timezone.utc),
            )
            active_subscription.save()

            # Create email for customer.
            customer_mail = active_subscription.user.email
            subject = render_to_string(
                "subscriptions/email_templates/invoice_paid_subject.txt",
                {
                    "invoice": invoice,
                },
            )
            body = render_to_string(
                "subscriptions/email_templates/invoice_paid_body.txt",
                {
                    "invoice": invoice,
                    "contact_email": settings.DEFAULT_FROM_EMAIL,
                },
            )
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [customer_mail],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found")

    if event_type == "invoice.payment_failed":
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        # Create email for customer.
        if data_object["attempt_count"] > 0:
            customer_id = data_object["customer"]
            freebees_customer = UserProfile.objects.get(
                stripe_customer_id=customer_id
            )

            name = data_object["customer_name"]

            customer_email = freebees_customer.user.email
            subject = render_to_string(
                "subscriptions/email_templates/payment_failed_subject.txt"
            )
            body = render_to_string(
                "subscriptions/email_templates/payment_failed_body.txt",
                {
                    "name": name,
                    "contact_email": settings.DEFAULT_FROM_EMAIL,
                },
            )
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [customer_email],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found")

    if event_type == "customer.subscription.deleted":
        # Use to send customer an email informing them and change subscription
        customer_id = data_object["customer"]
        freebees_customer = UserProfile.objects.get(
            stripe_customer_id=customer_id
        )

        # Find user subscription.
        subscription_id = data_object["id"]
        subscription = StripeSubscription.objects.get(
            subscription_id=subscription_id
        )

        # Find most recent invoice for customer details.
        invoice = subscription.invoice_set.all().order_by("current_end")[0]

        cancelled = timezone.now()

        subscription.end_date = cancelled
        subscription.save()

        # Construct email.
        customer_email = freebees_customer.user.email
        subject = render_to_string(
            "subscriptions/email_templates/subscription_deleted_subject.txt",
            {"invoice": invoice},
        )
        body = render_to_string(
            "subscriptions/email_templates/subscription_deleted_body.txt",
            {
                "invoice": invoice,
                "subscription": subscription,
                "cancelled": cancelled,
                "contact_email": settings.DEFAULT_FROM_EMAIL,
            },
        )
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [customer_email],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse("Invalid header found")

    if event_type == "customer.subscription.updated":
        # set up email to tell customer they have a new subscription.
        customer_id = data_object["customer"]

        freebees_customer = UserProfile.objects.get(
            stripe_customer_id=customer_id
        )

        today = timezone.now()

        # if the user has any active subscriptions, else return staus 200.
        if freebees_customer.has_active_subscription:
            subscription = freebees_customer.stripesubscription_set.filter(
                end_date__gte=today
            )[0]
        else:
            return HttpResponse({"status": "success"})

        # Only updates if cancel at end is different to the retrieved value.
        # Prevents unneccessary calls during new subscriptions, etc.
        if subscription.cancel_at_end == data_object["cancel_at_period_end"]:
            return HttpResponse({"status": "success"})
        else:
            if data_object["cancel_at_period_end"]:
                subscription.cancel_at_end = True
                subscription.save()

                # Create email for customer.

                subject = render_to_string(
                    "subscriptions/email_templates/sub_cancelled_subject.txt",
                )
                body = render_to_string(
                    "subscriptions/email_templates/sub_cancelled_body.txt",
                    {
                        "subscription": subscription,
                        "contact_email": settings.DEFAULT_FROM_EMAIL,
                    },
                )
            else:
                subscription.cancel_at_end = False
                subscription.save()

                # Set as variable as line too long for pep8 otherwise.
                sub_reactivated_subject = (
                    "subscriptions/email_templates/sub_reactivated_subject.txt"
                )

                subject = render_to_string(
                    sub_reactivated_subject,
                    {"subscription": subscription},
                )
                body = render_to_string(
                    "subscriptions/email_templates/sub_reactivated_body.txt",
                    {
                        "subscription": subscription,
                        "contact_email": settings.DEFAULT_FROM_EMAIL,
                    },
                )

            customer_email = freebees_customer.user.email
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [customer_email],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found")
    return JsonResponse({"status": "success"})
