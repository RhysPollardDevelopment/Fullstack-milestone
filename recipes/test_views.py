from django.test import TestCase
from unittest.mock import patch
from .models import Recipe
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import tempfile

from django.contrib.auth.models import User
from products.models import Product
from subscriptions.models import StripeSubscription


class TestProductViews(TestCase):
    # Mocking create to avoid calling stripe.
    @patch("stripe.Customer.create")
    def setUp(self, mock_create):
        """Creates a user object to use in testing"""
        # Mocks the return value for fake Customer.create function.
        mock_create.return_value = {"id": "fakeID"}

        # Creates instance of User
        self.user = User.objects.create(
            username="testuser",
            email="testuser@test.com",
        )
        # Need to call set_password identified at https://stackoverflow.com/
        # questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
        self.user.set_password("12345")
        self.user.save()

        # Creates subscription instance so user can use has-active_subscription
        StripeSubscription.objects.create(
            subscription_id="testID",
            start_date=datetime(2020, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.user.userprofile,
        )

        # Test image file to satisfy recipe image field.
        # https://stackoverflow.com/questions/26298821/django-testing-
        # model-with-imagefield
        self.test_image = tempfile.NamedTemporaryFile(suffix="jpg").name

        self.product = Product.objects.create(
            name="Test product",
            description="Product test description",
            image=self.test_image,
        )

        # Create two recipes, one in past and one in future.
        self.recipe_unrestricted = Recipe.objects.create(
            title="test recipe",
            description="Recipe test description",
            publish_date=datetime(2020, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
            image=self.test_image,
            ingredients="Test for the text file.",
            instructions="Pseudo instructions for testing purposes.",
            featured_product=self.product,
        )
        Recipe.objects.create(
            title="too new",
            description="Should not load as date is not before now.",
            publish_date=datetime.now(tz=timezone.utc)
            + relativedelta(months=+2),
            image=self.test_image,
            ingredients="Test for the text file.",
            instructions="Pseudo instructions for testing purposes.",
            featured_product=self.product,
        )

        # Create recipe which is always within last 3 months.
        now = datetime.now(tz=timezone.utc)
        first_of_month = now + relativedelta(day=1)

        self.recipe_restricted = Recipe.objects.create(
            title="Restricted",
            description="Recipe test description",
            publish_date=first_of_month,
            image=self.test_image,
            ingredients="Test for the text file.",
            instructions="Pseudo instructions for testing purposes.",
            featured_product=self.product,
        )

    def test_get_all_recipes(self):
        """
        Should test that the view is being processed correctly and loading
        the relevant template.
        Only recipes with a publish date before today should be loaded.
        """
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes.html")
        # Test that view only retrieves recipes before todays date.
        self.assertEqual(response.context["recipes"].count(), 2)

    def test_get_recipe_detail_page_no_restrictions(self):
        """
        Should be able to load a recipe detail page with 200 status.
        """
        response = self.client.get(
            f"/recipes/{self.recipe_unrestricted.title}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")
        self.assertEqual(response.context["restricted"], False)

    def test_get_restricted_recipe_detail_unsubscribed(self):
        """
        Test for unsubscribed/anonymous users accessing recipe_details, should
        have access but the restricted variable should equal true as this will
        determine whether any content is blocked.
        """
        response = self.client.get(f"/recipes/{self.recipe_restricted.title}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")
        self.assertEqual(response.context["restricted"], True)

    def test_get_restricted_recipe_detail_subscribed(self):
        """
        Test for subscribed users accessing recipe_details, should
        have full access as restricted variable is False.
        """
        # Log in user as must be authenticated and subscribed
        self.client.login(username="testuser", password="12345")

        # Assert
        response = self.client.get(f"/recipes/{self.recipe_restricted.title}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")
        self.assertEqual(response.context["restricted"], False)
