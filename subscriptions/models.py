from django.db import models
from profiles.models import UserProfile
import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta

# Create your models here.


class Subscription(models.Model):
    """ """

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
        self.cancel_date = datetime.now()
        self.expiry_date = self.start_date + relativedelta(months=+2)

    # What is user restarts and has subscription ending? Need to
    # be able to start from end of previous subscription
