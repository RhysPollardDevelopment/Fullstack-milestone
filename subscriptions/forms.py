from django import forms


# Majority of code used from code-institue boutique-ado project work.
class SubscriptionForm(forms.Form):

    full_name = forms.CharField(label="Your Name", max_length=100)
    phone_number = forms.CharField(max_length=13)
    street_address1 = forms.CharField(max_length=80)
    street_address2 = forms.CharField(max_length=80)
    town_or_city = forms.CharField(max_length=40)
    county = forms.CharField(max_length=80, required=False)
    postcode = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "full_name": "Full name",
            "phone_number": "Phone Number",
            "street_address1": "Street Address 1",
            "street_address2": "Street Address 2",
            "town_or_city": "Town or City",
            "county": "County",
            "postcode": "Postal Code",
        }

        self.fields["phone_number"].widget.attrs["autofocus"] = True
        for field in self.fields:
            placeholder = f"{placeholders[field]}"
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs[
                "class"
            ] = "border-black rounded-0 profile-form-input"
            self.fields[field].label = False


# Majority of code used from code-institue boutique-ado project work.
class BillingAddressForm(forms.Form):

    billing_full_name = forms.CharField(label="Your Name", max_length=100)
    billing_phone_number = forms.CharField(max_length=13)
    billing_address1 = forms.CharField(max_length=80)
    billing_address2 = forms.CharField(max_length=80)
    billing_town_or_city = forms.CharField(max_length=40)
    billing_county = forms.CharField(max_length=80, required=False)
    billing_postcode = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "billing_full_name": "Full name",
            "billing_phone_number": "Phone Number",
            "billing_address1": "Street Address 1",
            "billing_address2": "Street Address 2",
            "billing_town_or_city": "Town or City",
            "billing_county": "County",
            "billing_postcode": "Postal Code",
        }
        self.fields["billing_phone_number"].widget.attrs["autofocus"] = True
        for field in self.fields:
            placeholder = f"{placeholders[field]}"
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs[
                "class"
            ] = "border-black rounded-0 profile-form-input"
            self.fields[field].label = False
