from django.test import TestCase
from .models import Recipe


class TestRecipeModels(TestCase):
    def test_recipe_to_string(self):
        """Tests overloaded string function"""
        recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test description for fake recipe.",
        )
        self.assertEqual(str(recipe), recipe.title)
