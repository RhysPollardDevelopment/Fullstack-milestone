from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from subscriptions.models import Subscription


class TestUserProfileModels(TestCase):
    def setUp(self):
        User.objects.create(username="testuser", password="testpassword")

    def test_UserProfile_active_subscription_False_on_creation(self):
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

    def test_UserProfile_only_one_active_subscription_True(self):
        """Tests whether has active subscription is correctly called"""
        newuser = User.objects.get(username="testuser")
        profile3 = UserProfile.objects.create(user=newuser)
        sub1 = Subscription.objects.create(user_profile=profile3)
        sub1.cancel()
        sub1.save()
        self.assertEqual(profile3.has_active_subscription, False)

    # def test_UserProfile_only_one_active_subscription_True(self):
    #     """Tests whether has active subscription is correctly called"""
    #     newuser = User.objects.get(username="testuser")
    #     profile = UserProfile.objects.create(user=newuser)
    #     sub1 = Subscription.objects.create(user_profile=profile)
    #     sub1.cancel()
    #     sub2 = Subscription.objects.create(user_profile=profile)
    #     sub2.cancel()
    #     sub3 = Subscription.objects.create(user_profile=profile)
    #     self.assertEqual(profile.has_active_subscription, True)
