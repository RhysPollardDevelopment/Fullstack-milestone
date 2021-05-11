from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    User profile model contains user delivery, payment and subscription
    information along with means to update.

    User is required, address is optional.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True
    )
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)

    # Checks if there is an active subscription with an expiry date
    # after or equal to today.
    @property
    def has_active_subscription(self):
        active_subscriptions = UserProfile.objects.filter(
            subscription__expiry_date__isnull=True
        )
        print(active_subscriptions.explain())
        if active_subscriptions.count() > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.user.username
