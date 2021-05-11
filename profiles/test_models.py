from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from subscriptions.models import Subscription


class TestUserProfileModels(TestCase):
    def setUp(self):
        """Creates User object for each new account profile."""
        User.objects.create(username="testuser", password="testpassword")

    def test_UserProfile_active_subscription_False_on_creation(self):
        """
        Tests that user has no active subscriptions upon profile creation.
        """
        newuser = User.objects.get(username="testuser")
        profile = UserProfile.objects.create(user=newuser)
        self.assertEqual(profile.has_active_subscription, False)

    def test_UserProfile_active_subscription_True(self):
        """
        Tests if user with an active subscription correctly calls the
        has_active_subscription property.
        """
        newuser = User.objects.get(username="testuser")
        profile = UserProfile.objects.create(user=newuser)

        # Assigns subscription to profile Userprofile
        Subscription.objects.create(user_profile=profile)

        self.assertEqual(profile.has_active_subscription, True)

    def test_UserProfile_correct_subscription_status_if_cancelled(self):
        """
        Tests that when a subscription is cancelled the userprofile property
        correctly registers the change to false for active subscritpion.
        """
        newuser = User.objects.get(username="testuser")
        profile3 = UserProfile.objects.create(user=newuser)
        subscription = Subscription.objects.create(user_profile=profile3)

        # Subscription is cancelled and change saved to database.
        subscription.cancel()
        subscription.save()

        # Assert: As subscription is cancelled, should produce false result.
        self.assertEqual(profile3.has_active_subscription, False)

    def test_UserProfile_only_one_active_subscription_True(self):
        """Tests whether has active subscription is correctly called"""
        newuser = User.objects.get(username="testuser")
        profile = UserProfile.objects.create(user=newuser)

        # First subscription is added and cancelled before saving to database
        subscription = Subscription.objects.create(user_profile=profile)
        subscription.cancel()
        subscription.save()

        # Second subscription is added and cancelled before saving to database
        subscription2 = Subscription.objects.create(user_profile=profile)
        subscription2.cancel()
        subscription2.save()

        # Third subscription is added but not cancelled to simulate
        # re-subscribing to the service.
        Subscription.objects.create(user_profile=profile)

        # Number of subscriptions without expiry_dates is counted and checked.
        # Confirms number of subscriptions and profile deems self subscribed.
        active_subscriptions = profile.subscription_set.filter(
            expiry_date__isnull=True
        ).count()
        self.assertEqual(profile.has_active_subscription, True)
        self.assertEqual(active_subscriptions, 1)

    def test_Userprofile_string_overload(self):
        """Tests overloaded string method"""
        newuser = User.objects.get(username="testuser")
        profile = UserProfile.objects.create(user=newuser)
        self.assertEqual(str(profile), profile.user.username)
