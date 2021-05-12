from django.db import models
from profiles.models import UserProfile
from django.utils import timezone
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
