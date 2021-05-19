from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    User profile model contains user delivery, payment and subscription
    information along with means to update.

    User is required, address is optional.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=13, null=True, blank=True
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
        active_subscriptions = self.subscription_set.filter(
            expiry_date__isnull=True
        )
        return active_subscriptions.count() > 0

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    create or update user
    """
    if created:
        UserProfile.objects.create(user=instance)
    # existing users, just save profile
    instance.userprofile.save()
