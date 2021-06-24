from django.db import models
from profiles.models import UserProfile
from recipes.models import Recipe


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
    cancel_at_end = models.BooleanField(default=False)

    def __str__(self):
        return self.subscription_id


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

    @property
    def related_recipe(self):
        recipes = Recipe.objects.all()
        for recipe in recipes:
            d = recipe.publish_date
            if self.current_start < d and self.current_end > d:
                return recipe

    def __str__(self):
        return self.invoice_number
