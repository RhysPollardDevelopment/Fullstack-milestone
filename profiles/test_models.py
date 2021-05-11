from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from subscriptions.models import Subscription


class TestUserProfileModels(TestCase):
    def setUp(self):
        User.objects.create(username="testuser", password="testpassword")

    def test_UserProfile_active_subscription_False(self):
        """Tests whether has active subscription is correctly called"""
        User.objects.create(username="testuser2", password="testpassword")
        newuser = User.objects.get(username="testuser2")
        profile = UserProfile.objects.create(user=newuser)
        self.assertEqual(profile.has_active_subscription, False)

    def test_UserProfile_active_subscription_True(self):
        """Tests whether has active subscription is correctly called"""
        newuser = User.objects.get(username="testuser")
        profile = UserProfile.objects.create(user=newuser)
        Subscription.objects.create(user_profile=profile)
        self.assertEqual(profile.has_active_subscription, True)
