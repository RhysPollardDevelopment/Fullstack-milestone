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
        """
        Assesses whether help_text has been correctly set.
        """
        # https://stackoverflow.com/questions/24344981/how-to-change-help-
        # text-of-a-django-form-field

        # Above link helped figure out how to access help_text.
        self.assertEqual(
            self.form.fields["publish_date"].help_text,
            "When this recipe will become active to users.",
        )
