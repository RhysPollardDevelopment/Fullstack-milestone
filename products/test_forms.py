from django.test import TestCase
from .forms import ProductForm, CompanyForm


class TestProductForm(TestCase):
    def setUp(self):
        self.form = ProductForm()

    def test_form_field_has_correct_placeholder(self):
        """
        Checks that the placeholder has been correctly set on form
        initialization.
        """

        self.assertEqual(
            self.form.fields["flavour"].widget.attrs["placeholder"],
            "Flavour profile",
        )

    def test_form_help_text_is_correct(self):
        """
        Assesses whether help_text has been correctly set.
        """
        # https://stackoverflow.com/questions/24344981/how-to-change-help-
        # text-of-a-django-form-field

        # Above link helped figure out how to access help_text.
        self.assertEqual(
            self.form.fields["texture"].help_text,
            "One word descriptions seperated by commas.",
        )


class TestCompanyForm(TestCase):
    def setUp(self):
        self.form = CompanyForm()

    def test_form_field_has_correct_placeholder(self):
        """
        Checks that the placeholder has been correctly set on form
        initialization.
        """

        self.assertEqual(
            self.form.fields["description"].widget.attrs["placeholder"],
            "Company description",
        )

    def test_form_help_text_is_correct(self):
        """
        Assesses whether help_text has been correctly set.
        """
        # https://stackoverflow.com/questions/24344981/how-to-change-help-
        # text-of-a-django-form-field

        # Above link helped figure out how to access help_text.
        self.assertEqual(
            self.form.fields["company_url"].help_text,
            "Please ensure this is a valid web address.",
        )
