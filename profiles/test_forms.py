from django.test import TestCase
from .forms import UserProfileForm


class TestUserProfileForm(TestCase):
    def test_form_fields_exclude(self):
        """
        Uses variable to check whether the return value of .get() on form
        fields is None as should be excluded.
        """
        form = UserProfileForm()
        user_field = form.fields.get("user")
        stripe_customer_field = form.fields.get("stripe_customer_id")
        self.assertIsNone(user_field)
        self.assertIsNone(stripe_customer_field)

    def test_form_field_has_correct_placeholder(self):
        """
        Checks that the placeholder has been correctly set on form
        initialization.
        """
        form = UserProfileForm()
        self.assertEqual(
            form.fields["default_postcode"].widget.attrs["placeholder"],
            "Postal Code",
        )

    def test_form_data_is_invalid(self):
        """
        Ensures basic validation is being performed on input values.
        """
        data = {
            "default_phone_number": "012345672222222222222222222222222",
            "default_street_address1": "46",
            "default_street_addre": "default street",
            "default_town_or_city": "default town",
            "default_county": "default town",
            "default_postcode": "DEF 4U1T",
        }
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
