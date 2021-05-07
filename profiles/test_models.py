from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class TestUserProfileModels(TestCase):
    def setUp(self):
        newuser = User.objects.create(
            username="testuser",
            password="testpassword"
        )
        profile = UserProfile.objects.create(user=newuser)

    def test_UserProfile_to_string(self):
        """Tests overloaded string function"""
        self.assertEqual(str(profile), profile.user.username)

    def test_UserProfile_active_subscription_false(self):
        
