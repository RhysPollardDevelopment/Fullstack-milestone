from django.db import models
from profiles.models import UserProfile
from django.utils import timezone, tree
from dateutil.relativedelta import relativedelta

# Create your models here.


class Subscription(models.Model):
    """
    Records start date, end date and cancellation date for particular
    subscription. Cancel method sets cancellation and expiry date.

    All fields optional, start_date is generated on creation.
    """

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True
    )
    # auto_add_not takes time of instance creation and makes it date-time.
    # found at https://docs.djangoproject.com/en/3.2/ref/models/fields/#django
    # .db.models.DateTimeField
    start_date = models.DateTimeField(auto_now_add=True)

    cancel_date = models.DateTimeField(blank=True, null=True)

    expiry_date = models.DateTimeField(blank=True, null=True)

    def cancel(self):
        """
        Sets cancel_date and expiry_date, for admin to see and for UserProfile
        to check if has an active subscription respectively.

        Calculates difference between start and cancel dates and applies to
        the start date to create expiry date.
        """
        self.cancel_date = timezone.now()
        difference = relativedelta(self.cancel_date, self.start_date)

        # 1 added to the months delta as relativedelta does not count to next
        # months date (i.e. the 24th) when calculated so is month short.
        difference.months = difference.months + 1
        self.expiry_date = self.start_date + relativedelta(
            months=+difference.months
        )

    # What is user restarts and has subscription ending? Need to
    # be able to start from end of previous subscription


class StripeSubscription(models.Model):
    """
    Stripe subscription model contains key information for individual stripe
    subscriptions which have been created, only one can be active at once.

    Subscription_id, start_date and end_date are required fields and set in
    response to stripe webhooks.
    """

    subscription_id = models.CharField(
        max_length=255,
        help_text="Stripe subscription Id for communicating with stripe.",
    )
    start_date = models.DateTimeField(
        help_text="The start date of the subscription."
    )
    end_date = models.DateTimeField(
        help_text="The end date of the subscription."
    )
    stripe_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Invoice(models.Model):
    """
    Local record of stripe invoice, connected to userprofile and has connection
    to monthly subscription reward also.

    All fields are required and set on invoice.paid webhook.
    """

    stripe_subscription = models.ForeignKey(
        StripeSubscription, null=True, on_delete=models.CASCADE
    )
    invoice_number = models.CharField(
        max_length=255, null=True, help_text="Stripe invoice code."
    )

    current_start = models.DateTimeField(
        null=True, help_text="The start date of current invoice period."
    )
    current_end = models.DateTimeField(
        null=True, help_text="The end date of current invoice period."
    )
    delivery_name = models.CharField(
        null=True,
        max_length=255,
        help_text="Name of person whom delivery is for.",
    )
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    town_or_city = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
