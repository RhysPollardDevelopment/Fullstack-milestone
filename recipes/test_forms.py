from django.test import TestCase
from .forms import RecipeForm


class TestRecipeForm(TestCase):
    def setUp(self):
        self.form = RecipeForm()

    def test_form_field_has_correct_placeholder(self):
        """
        Checks that the placeholder has been correctly set on form
        initialization.
        """

        self.assertEqual(
            self.form.fields["description"].widget.attrs["placeholder"],
            "Recipe description",
        )

    def test_form_help_text_is_correct(self):
        self.assertEqual(
            self.form.fields["publish_date"].help_text,
            "When this recipe will become active to users.",
        )
