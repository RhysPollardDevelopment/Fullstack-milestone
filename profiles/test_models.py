from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, timezone
from unittest.mock import patch
from subscriptions.models import StripeSubscription


class TestProfileModels(TestCase):
    @patch("stripe.Customer.create")
    def setUp(self, mock_create):
        """Creates User object for each new account profile."""
        mock_create.return_value = {"id": "fakeID"}
        self.user = User.objects.create(
            username="tester", password="testpassword"
        )
        self.user.save()
        self.profile = self.user.userprofile

    def test_UserProfile_active_subscription_False_on_creation(self):
        """
        Tests that user has no active subscriptions upon profile creation.
        """
        self.assertEqual(self.profile.has_active_subscription, False)

    def test_UserProfile_active_subscription_True(self):
        """
        Tests if user with an active subscription correctly calls the
        has_active_subscription property.
        """
        # Assigns subscription to profile Userprofile
        self.stripe_subscription = StripeSubscription.objects.create(
            subscription_id="testsub",
            start_date=datetime(2030, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.profile,
        )

        self.assertEqual(self.profile.has_active_subscription, True)

    def test_UserProfile_correct_subscription_status_if_cancelled(self):
        """
        Tests that when a subscription is cancelled the userprofile property
        correctly registers the change to false for active subscritpion.
        """

        # Assert: As subscription is cancelled, should produce false result.
        self.assertEqual(self.profile.has_active_subscription, False)

    def test_UserProfile_only_one_active_subscription_True(self):
        """Tests whether has active subscription is correctly called"""
        # Three subscriptions are created out of order but with correct dates
        # to simulate multiple subscription periods.
        StripeSubscription.objects.create(
            subscription_id="testsub",
            start_date=datetime(2020, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2020, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.profile,
        )

        StripeSubscription.objects.create(
            subscription_id="testsub2",
            start_date=datetime(2021, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2023, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.profile,
        )

        StripeSubscription.objects.create(
            subscription_id="testsub3",
            start_date=datetime(2020, 12, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2021, 2, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.profile,
        )

        # Number of subscriptions eith end_dates after today are counted.
        # Confirms number of subscriptions and profile deems self subscribed.
        today = datetime.now(tz=timezone.utc)
        active_subscriptions = self.profile.stripesubscription_set.filter(
            end_date__gte=today
        ).count()
        self.assertEqual(self.profile.has_active_subscription, True)
        self.assertEqual(active_subscriptions, 1)

    def test_Userprofile_string_overload(self):
        """Tests overloaded string method"""
        self.assertEqual(str(self.profile), self.user.username)

    def test_auto_create_update_user_function(self):
        self.assertIsNotNone(self.user.userprofile)
