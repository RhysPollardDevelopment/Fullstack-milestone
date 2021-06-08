from django.test import TestCase
from .models import Recipe
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from subscriptions.models import StripeSubscription


class TestProductViews(TestCase):
    def setUp(self):
        """Creates a user object to use in testing"""
        self.user = User.objects.create(
            username="testuser",
            email="testuser@test.com",
        )
        # Need to call set_password identified at https://stackoverflow.com/
        # questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
        self.user.set_password("12345")
        self.user.save()
        StripeSubscription.objects.create(
            subscription_id="testID",
            start_date=datetime(2020, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.user.userprofile,
        )

    def test_get_all_recipes(self):
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes.html")
        self.assertIsNotNone(response.context["recipes"])

    def test_get_recipe_page(self):
        recipe = Recipe.objects.create(
            title="test recipe", description="Recipe test description"
        )
        response = self.client.get(f"/recipes/{recipe.title}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_page.html")

    def test_get_restricted_recipe_anonymous(self):
        now = datetime.now(tz=timezone.utc)
        first_of_month = now + relativedelta(day=1)
        recipe = Recipe.objects.create(
            title="test recipe",
            description="Recipe test description",
            publish_date=first_of_month,
        )
        response = self.client.get(f"/recipes/{recipe.title}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_page.html")
        self.assertEqual(response.context["restricted"], True)

    def test_get_restricted_recipe_subscribed(self):
        now = datetime.now(tz=timezone.utc)
        first_of_month = now + relativedelta(day=1)
        recipe = Recipe.objects.create(
            title="test recipe",
            description="Recipe test description",
            publish_date=first_of_month,
        )
        self.client.login(username="testuser", password="12345")
        response = self.client.get(f"/recipes/{recipe.title}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_page.html")
        self.assertEqual(response.context["restricted"], False)
