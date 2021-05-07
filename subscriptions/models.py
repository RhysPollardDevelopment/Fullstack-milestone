from django.db import models
from profiles.models import UserProfile
from dateutil import relativedelta

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

    def set_expiry_date():
        end_date = start_date + relativedelta(month=1)
        return end_date

    expiry_date = models.DateTimeField(default=set_expiry_date)
    status = models.CharField

    # What is user restarts and has subscription ending? Need to
    # be able to start from end of previous subscription
