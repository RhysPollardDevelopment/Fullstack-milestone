from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from datetime import datetime, timezone

from subscriptions.models import StripeSubscription


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
    @patch("stripe.Customer.create")
    def setUp(self, mock_create):
        """Creates a user object to use in testing"""
        mock_create.return_value = {"id": "fakeID"}
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
        """Confirms user has all required to log in."""
        logged_in = self.client.login(username="testuser", password="12345")
        self.assertTrue(logged_in)

    def test_get_user_profile(self):
        """
        Test that logged in user can access main profile page.
        """
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/userprofile.html")

    def test_get_update_details_page(self):
        """
        Test that user can route to their details page to edit information.
        """
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/update_address/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/update_address.html")

    def test_can_update_details(self):
        """
        User should be able to send new information in post method and update
        their details, results should redirect user to profile page.
        """
        self.client.login(username="testuser", password="12345")
        self.user.userprofile.default_street_address2 = "test road"
        response = self.client.post(
            "/profiles/update_address/",
            {
                "default_street_address2": "test street",
            },
        )
        # Loads updated object from database to compare street_address2
        updated = User.objects.get(username="testuser")
        self.assertRedirects(response, "/profiles/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            updated.userprofile.default_street_address2, "test street"
        )

    def test_get_password_change_done_page(self):
        """
        Upon successfully changing password in password_change form, user
        should be redirected to password done page.
        """
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/password_change_done")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "allauth/account/password_change_done.html"
        )

    def test_get_all_saved_recipes(self):
        """
        If user has recipes saved then they should be able to acce3ss a page
        with all recipes saved shown.
        """
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/my_recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/my_recipes.html")

    def test_get_subscription_history(self):
        """
        Shows user they're subscription history page.
        """
        StripeSubscription.objects.create(
            subscription_id="testID",
            start_date=datetime(2020, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.user.userprofile,
        )

        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/subscription_history/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/subscription_history.html")
