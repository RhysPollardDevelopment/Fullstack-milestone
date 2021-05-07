from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class TestUserProfileModels(TestCase):
    def test_UserProfile_to_string(self):
        """Tests overloaded string function"""
        newuser = User.objects.create(
            username="testuser", password="testpassword"
        )
        profile = UserProfile.objects.create(user=newuser)
        self.assertEqual(str(profile), profile.user.username)
