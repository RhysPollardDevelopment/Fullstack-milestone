from django import forms
from .models import UserProfile


# Majoriy of code used from code-institue boutique-ado project work.
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = (
            "user",
            "stripe_customer_id",
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "default_phone_number": "Phone Number",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_town_or_city": "Town or City",
            "default_county": "County",
            "default_postcode": "Postal Code",
        }

        self.fields["default_phone_number"].widget.attrs["autofocus"] = True
        for field in self.fields:
            placeholder = f"{placeholders[field]}"
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs[
                "class"
            ] = "border-black rounded-0 profile-form-input"
            self.fields[field].label = False
