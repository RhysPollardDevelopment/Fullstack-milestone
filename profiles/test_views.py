from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile


def create_test_user(client):
    user_data = {
        "username": "testuser",
        "password": "12345",
        "password2": "12345",
    }
    client.post(reverse("users:register"), data=user_data)


def login_sample_user(client):
    logged_in = client.post(
        reverse("users:login"),
        data={
            "username": "testuser",
            "password": "12345",
        },
    )
    return logged_in


class TestProfileViews(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="testuser@test.com",
        )
        # Need to call set_password identified at https://stackoverflow.com/
        # questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
        self.user.set_password("12345")
        self.user.save()
        self.client = Client()

    def test_user_loggedin(self):
        logged_in = self.client.login(username="testuser", password="12345")
        self.assertTrue(logged_in)

    def test_get_user_profile(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/userprofile.html")
