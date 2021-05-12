from datetime import datetime
from django.test import TestCase
from .models import Subscription
from django.utils import timezone
from unittest import mock


mocked_start = datetime(2020, 9, 24, 10, 15, 30, tzinfo=timezone.utc)
mocked_now = datetime(2021, 5, 12, 13, 30, 0, tzinfo=timezone.utc)
mocked_after_24th = datetime(2021, 5, 26, 13, 30, 0, tzinfo=timezone.utc)
mocked_same_day_of_month = datetime(2021, 5, 24, 11, 0, 0, tzinfo=timezone.utc)


def mock_start():
    return mocked_start


def mock_now():
    return mocked_now


def mock_post_24th():
    return mocked_after_24th


# @mock.patch("django.utils.timezone.now", side_effect=mocked_date)
class TestSubscriptionModel(TestCase):
    @mock.patch("django.utils.timezone.now", side_effect=mock_start)
    def setUp(self, *args):
        self.new_sub = Subscription.objects.create()

    @mock.patch("django.utils.timezone.now", side_effect=mock_now)
    def test_subscription_cancel_method(self, *args):

        self.new_sub.cancel()
        self.new_sub.save()
        expiration = datetime(2021, 5, 24, 10, 15, 30, tzinfo=timezone.utc)
        self.assertEqual(self.new_sub.start_date, mocked_start)
        self.assertEqual(self.new_sub.expiry_date, expiration)
        self.assertEqual(self.new_sub.cancel_date, mocked_now)

    @mock.patch("django.utils.timezone.now", side_effect=mock_post_24th)
    def test_cancellation_after_start_day(self, *args):
        self.new_sub.cancel()
        self.new_sub.save()
        expiration = datetime(2021, 6, 24, 10, 15, 30, tzinfo=timezone.utc)
        self.assertEqual(self.new_sub.start_date, mocked_start)
        self.assertEqual(self.new_sub.expiry_date, expiration)
        self.assertEqual(self.new_sub.cancel_date, mocked_after_24th)
