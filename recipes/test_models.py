from django.test import TestCase
from .models import Recipe
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


class TestRecipeModels(TestCase):
    def test_recipe_to_string(self):
        """Tests overloaded string function"""
        recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test description for fake recipe.",
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_restricted_property(self):
        """Tests that recipe can correctly discern if restricted"""
        unrestricted = Recipe.objects.create(
            title="unrestricted",
            description="Test description for fake recipe.",
            publish_date=datetime(
                2020, 5, 6, 7, 30, 25, 0, tzinfo=timezone.utc
            ),
        )
        restricted = Recipe.objects.create(
            title="Restricted",
            description="Test description for fake recipe.",
            publish_date=(
                datetime.now(tz=timezone.utc) + relativedelta(days=-2)
            ),
        )

        self.assertFalse(unrestricted.is_restricted)
        self.assertTrue(restricted.is_restricted)
