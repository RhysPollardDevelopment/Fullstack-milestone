from products.models import Product
from django.db import models
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


class Recipe(models.Model):
    """
    Model for recipes to add to the site, title, description and image are
    all required attributes.

    Publish date used to determine if loaded to recipes page and for linking
    to invoices of subscribed users.
    """

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=400)
    ingredients = models.TextField(null=True)
    instructions = models.TextField(null=True)
    image = models.ImageField(null=True)
    publish_date = models.DateTimeField(
        null=True,
        help_text="Date used to determine loading date and user access.",
    )
    featured_product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL
    )

    @property
    def is_restricted(self):
        three_months_ago = datetime.now(tz=timezone.utc) + relativedelta(
            months=-3
        )

        # If recipe publish date is within last 3 months, is restricted to
        # users without subscriptions.
        return self.publish_date > three_months_ago

    def __str__(self):
        return self.title
