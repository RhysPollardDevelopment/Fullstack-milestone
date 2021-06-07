from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Invoice, StripeSubscription, Subscription
from django.utils import timezone
from unittest import mock


# Suggestion for layout when using mock for timezone.now found at:
# https://snakeycode.wordpress.com/2015/11/04/mocking-django-timezone/
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


class TestSubscriptionModel(TestCase):
    @mock.patch("django.utils.timezone.now", side_effect=mock_start)
    @mock.patch("stripe.Customer.create")
    def setUp(self, mock_create, *args):
        """
        Uses mock to set start date of new object to 29/09/2020 10:15:30.
        Necessary as start_date is automatic and un-editable.
        """
        mock_create.return_value = {"id": "fakeID"}
        self.new_sub = Subscription.objects.create()
        self.user = User.objects.create(
            username="testuser",
            email="testuser@test.com",
        )
        # Need to call set_password identified at https://stackoverflow.com/
        # questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
        self.user.set_password("12345")
        self.user.save()
        self.stripe_subscription = StripeSubscription.objects.create(
            subscription_id="testsub",
            start_date=datetime(2030, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.user.userprofile,
        )

    @mock.patch("django.utils.timezone.now", side_effect=mock_now)
    def test_subscription_cancel_method(self, *args):
        """
        Mocks a date in the future and compares the calculated expiration
        date to a pre-determined value.
        """
        self.new_sub.cancel()
        self.new_sub.save()
        expiration = datetime(2021, 5, 24, 10, 15, 30, tzinfo=timezone.utc)
        self.assertEqual(self.new_sub.start_date, mocked_start)
        self.assertEqual(self.new_sub.expiry_date, expiration)
        self.assertEqual(self.new_sub.cancel_date, mocked_now)

    @mock.patch("django.utils.timezone.now", side_effect=mock_post_24th)
    def test_cancellation_after_start_day(self, *args):
        """
        Mocks a date in the future and compares the calculated expiration
        date to a pre-determined value after the start date's day value.
        """
        self.new_sub.cancel()
        self.new_sub.save()
        expiration = datetime(2021, 6, 24, 10, 15, 30, tzinfo=timezone.utc)
        self.assertEqual(self.new_sub.start_date, mocked_start)
        self.assertEqual(self.new_sub.expiry_date, expiration)
        self.assertEqual(self.new_sub.cancel_date, mocked_after_24th)

    def test_stripesubscription_to_string(self):
        """Test overloaded string functions"""
        self.assertEqual(
            str(self.stripe_subscription),
            self.stripe_subscription.subscription_id,
        )

    def test_invoice_to_string(self):
        """Test overloaded string functions"""
        test_invoice = Invoice.objects.create(
            stripe_subscription=self.stripe_subscription,
            invoice_number="testinvoice",
            delivery_name=self.user.username,
            address_1="1234",
            address_2="test lane",
            town_or_city="testington",
            county="greater testington",
            postcode="T35T",
        )
        self.assertEqual(
            str(test_invoice),
            test_invoice.invoice_number,
        )
