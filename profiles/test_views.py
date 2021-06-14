from django.test import TestCase, Client
from django.contrib.auth.models import User
from unittest.mock import patch
from datetime import datetime, timezone
import tempfile

from subscriptions.models import StripeSubscription, Invoice
from recipes.models import Recipe
from products.models import Product


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

    @patch("stripe.Customer.modify")
    @patch("stripe.Customer.retrieve")
    def test_get_update_details_page(self, mock_retrieve, mock_update):
        """
        Test that user can route to their details page to edit information.
        """

        self.client.login(username="testuser", password="12345")

        response = self.client.get("/profiles/update/address/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/update_address.html")
        self.assertEqual(mock_update.called, False)
        self.assertEqual(mock_retrieve.called, True)

    @patch("stripe.Customer.modify")
    @patch("stripe.Customer.retrieve")
    def test_can_update_details(self, mock_retrieve, mock_update):
        """
        User should be able to send new information in post method and update
        their details, results should redirect user to profile page.
        """
        self.client.login(username="testuser", password="12345")

        self.user.userprofile.default_street_address2 = "test road"

        response = self.client.post(
            "/profiles/update/address/",
            {
                "default_phone_number": "123456",
                "default_street_address1": "124",
                "default_street_address2": "test street",
                "default_town_or_city": "Fake town",
                "default_county": "Falsehood",
                "default_postcode": "T35T",
            },
        )
        # Loads updated object from database to compare street_address2
        updated = User.objects.get(username="testuser")
        self.assertRedirects(response, "/profiles/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            updated.userprofile.default_street_address2, "test street"
        )
        self.assertEqual(mock_update.called, True)
        self.assertEqual(mock_retrieve.called, True)

    @patch("stripe.Customer.modify")
    def test_can_update_billing(self, mock_update):
        """
        User should be able to send new information in post method and update
        their details, results should redirect user to profile page.
        """

        self.client.login(username="testuser", password="12345")

        self.user.userprofile.default_street_address2 = "test road"

        response = self.client.post(
            "/profiles/update/billing/",
            {
                "billing_address1": "987",
                "billing_address2": "billing street",
                "billing_town_or_city": "billtown",
                "billing_county": "Moneyshire",
                "billing_postcode": "81LL",
                "billing_phone_number": "12345678",
                "billing_full_name": "testuser",
            },
        )
        # Loads updated object from database to compare street_address2
        self.assertRedirects(response, "/profiles/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(mock_update.called, True)

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
        Shows user they're subscription history page, primarily invoices and
        monthly subscription bonuses such as recipes to access and products
        delivered.
        """
        # Creates all the data required to mock a subscription history.
        sub = StripeSubscription.objects.create(
            subscription_id="testID",
            start_date=datetime(2020, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.user.userprofile,
        )
        Invoice.objects.create(
            stripe_subscription=sub,
            invoice_number="123456",
            current_start=datetime(
                2021, 1, 10, 0, 0, 0, 0, tzinfo=timezone.utc
            ),
            current_end=datetime(2021, 2, 10, 0, 0, 0, 0, tzinfo=timezone.utc),
            delivery_name="test user",
            address_1="12",
            address_2="test street",
            town_or_city="test town",
            county="test county",
            postcode="T35T",
        )

        test_image = tempfile.NamedTemporaryFile(suffix="jpg").name

        product = Product.objects.create(
            name="Product",
            description="Product description",
            image=test_image,
        )

        recipe = Recipe.objects.create(
            title="recipe title",
            description="recipe description",
            image=test_image,
            publish_date=datetime(2021, 1, 15, tzinfo=timezone.utc),
            featured_product=product,
        )

        # Logs in user to test client.
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/profiles/subscription_history/")

        # Asserts that response is successfull and loads correct page.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/subscription_history.html")

        # Asserts that the invoice has been loaded in context with appropriate
        # recipe.
        invoices = response.context["invoices"][0]
        self.assertEqual(len(response.context["invoices"]), 1)
        self.assertEqual(recipe.title, invoices.recipe.title)
