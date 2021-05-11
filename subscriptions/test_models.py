from django.test import TestCase
from .models import Subscription
import datetime
from dateutil.relativedelta import relativedelta

# Create your tests here.


class TestSubscriptionModel(TestCase):
    def test_subscription_cancel_method(self):
        new_sub = Subscription.objects.create()
        expiration = new_sub.start_date + relativedelta(months=+2)
        new_sub.cancel()
        self.assertEqual(new_sub.expiry_date, expiration)
        self.assertEqual(new_sub.cancel_date, datetime.datetime.now())
