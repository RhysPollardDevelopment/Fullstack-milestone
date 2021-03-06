from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Invoice, StripeSubscription
from django.utils import timezone
from unittest import mock

from recipes.models import Recipe


class TestSubscriptionModel(TestCase):
    @mock.patch("stripe.Customer.create")
    def setUp(self, mock_create):
        """
        Uses mock to set start date of new object to 29/09/2020 10:15:30.
        Necessary as start_date is automatic and un-editable.
        """
        mock_create.return_value = {"id": "fakeID"}
        self.user = User.objects.create(
            username="testuser",
            email="testuser@test.com",
        )
        # Need to call set_password identified at https://stackoverflow.com/
        # questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
        self.user.set_password("12345")
        self.user.save()
        self.stripe_subscription = StripeSubscription.objects.create(
            subscription_id="testsub",
            start_date=datetime(2030, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.user.userprofile,
        )

    def test_stripesubscription_to_string(self):
        """Test overloaded string functions"""
        self.assertEqual(
            str(self.stripe_subscription),
            self.stripe_subscription.subscription_id,
        )

    def test_invoice_to_string(self):
        """Test overloaded string functions"""
        test_invoice = Invoice.objects.create(
            stripe_subscription=self.stripe_subscription,
            invoice_number="testinvoice",
            delivery_name=self.user.username,
            address_1="1234",
            address_2="test lane",
            town_or_city="testington",
            county="greater testington",
            postcode="T35T",
        )
        self.assertEqual(
            str(test_invoice),
            test_invoice.invoice_number,
        )

    def test_invoice_related_recipe_method(self):
        """Test if invoice can associate related recipe"""
        # Invoice should find a recipe as publish date between start and end.
        with_recipe = Invoice.objects.create(
            stripe_subscription=self.stripe_subscription,
            invoice_number="testinvoice",
            delivery_name=self.user.username,
            current_start=datetime(
                2020, 6, 6, 12, 30, 30, 0, tzinfo=timezone.utc
            ),
            current_end=datetime(
                2020, 7, 6, 12, 30, 30, 0, tzinfo=timezone.utc
            ),
            address_1="1234",
            address_2="test lane",
            town_or_city="testington",
            county="greater testington",
            postcode="T35T",
        )
        # Invoice should not have a recipe as too late.
        without_recipe = Invoice.objects.create(
            stripe_subscription=self.stripe_subscription,
            invoice_number="testinvoice",
            current_start=datetime(
                2020, 8, 8, 12, 30, 30, 0, tzinfo=timezone.utc
            ),
            current_end=datetime(
                2020, 9, 9, 12, 30, 30, 0, tzinfo=timezone.utc
            ),
            delivery_name=self.user.username,
            address_1="1234",
            address_2="test lane",
            town_or_city="testington",
            county="greater testington",
            postcode="T35T",
        )

        recipe = Recipe.objects.create(
            title="too new",
            description="Should not load as date is not before now.",
            publish_date=datetime(
                2020, 6, 28, 12, 30, 30, 0, tzinfo=timezone.utc
            ),
            ingredients="Test for the text file.",
            instructions="Pseudo instructions for testing purposes.",
        )

        self.assertEqual(with_recipe.related_recipe, recipe)
        self.assertEqual(without_recipe.related_recipe, None)
