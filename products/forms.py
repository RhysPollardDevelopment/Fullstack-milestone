from django import forms
from django.forms.widgets import TextInput
from .models import Product, Company


class ProductForm(forms.ModelForm):
    """
    Product model form used for CRUD operations in the database.
    """

    class Meta:
        model = Product
        exclude = ("product_code",)

        # Set up help texts for more complicated inputs.
        help_texts = {
            "texture": ("One word descriptions seperated by commas."),
            "flavour": ("One word descriptions seperated by commas."),
        }

        widgets = {
            "name": TextInput(attrs={"placeholder": "Name"}),
            "description": TextInput(
                attrs={"placeholder": "Product description"}
            ),
            "texture": TextInput(attrs={"placeholder": "Texture"}),
            "flavour": TextInput(attrs={"placeholder": "Flavour profile"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "border-black rounded-0"
            self.fields[field].label = False


class CompanyForm(forms.ModelForm):
    """
    Company model form used for CRUD operations in the database.
    """

    class Meta:
        model = Company
        fields = "__all__"

        # Set up help texts for more complicated inputs.
        help_texts = {
            "company_url": ("Please ensure this is a valid web address."),
        }

        widgets = {
            "name": TextInput(attrs={"placeholder": "Name"}),
            "description": TextInput(
                attrs={"placeholder": "Company description"}
            ),
            "county": TextInput(attrs={"placeholder": "Company county"}),
            "company_url": TextInput(
                attrs={"placeholder": "Company web address"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "border-black rounded-0"
            self.fields[field].label = False
