from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


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

    def test_get_update_details_page(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/update_address/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/update_address.html")

    def test_can_update_details(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            "/profiles/update_address/",
            {
                "default_street_address1": "123",
                "default_street_address2": "test street",
                "default_town_or_city": "testington",
                "default_county": "birmingtest",
                "default_postcode": "T35T",
            },
        )
        self.assertRedirects(response, "/profiles/")

    def test_get_change_password_page(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/change_password/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/change_password.html")

    def test_can_change_password(self):
        response = self.client.post("/profiles/change_password/")

    def test_get_all_saved_recipes(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/my_recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/my_recipes.html")

    def test_get_subscription_history(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/subscription_history/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/subscription_history.html")
