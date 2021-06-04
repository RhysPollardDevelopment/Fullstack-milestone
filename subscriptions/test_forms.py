from django.test import TestCase
from .forms import SubscriptionForm, BillingAddressForm


class TestSubscriptionForm(TestCase):
    def test_form_field_has_correct_placeholder(self):
        """
        Checks that the placeholder has been correctly set on form
        initialization.
        """
        form = SubscriptionForm()
        self.assertEqual(
            form.fields["town_or_city"].widget.attrs["placeholder"],
            "Town or City",
        )


class TestBillingAddressForm(TestCase):
    def test_form_field_has_correct_placeholder(self):
        """
        Checks that the placeholder has been correctly set on form
        initialization.
        """
        form = BillingAddressForm()
        self.assertEqual(
            form.fields["billing_phone_number"].widget.attrs["placeholder"],
            "Phone Number",
        )
