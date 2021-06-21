from django.test import TestCase
from .forms import ContactForm


class TestContractForm(TestCase):
    def test_form_field_has_correct_placeholder(self):
        """
        Checks that the placeholder has been correctly set on form
        initialization.
        """
        form = ContactForm()
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Name",
        )
