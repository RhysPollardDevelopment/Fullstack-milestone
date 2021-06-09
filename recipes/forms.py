from django import forms
from django.forms.widgets import TextInput
from .models import Recipe


class RecipeForm(forms.ModelForm):
    """
    Recipe model form used for CRUD operations in the database.
    """

    class Meta:
        model = Recipe
        # Selected individually to control order.
        fields = [
            "title",
            "description",
            "image",
            "ingredients",
            "instructions",
            "featured_product",
            "publish_date",
        ]

        # Set up help texts for more complicated inputs.
        help_texts = {
            "ingredients": (
                "Ensure that each instruction is entered onto a new line."
            ),
            "instructions": (
                "Ensure that each instruction is entered onto a new line."
            ),
            "publish_date": "When this recipe will become active to users.",
            "featured_product": "Select the associated honey product.",
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "Title"}),
            "description": TextInput(
                attrs={"placeholder": "Recipe description"}
            ),
            "ingredients": TextInput(attrs={"placeholder": "Ingredients list"}),
            "instructions": TextInput(
                attrs={"placeholder": "Instructions list"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs[
                "class"
            ] = "border-black rounded-0 profile-form-input"
            self.fields[field].label = False
