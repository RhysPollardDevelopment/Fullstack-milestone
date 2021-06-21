from django import forms
from django.forms.widgets import TextInput, Textarea
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
                "Ensure that each ingredient is entered onto a new line."
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
            "ingredients": Textarea(
                attrs={
                    "placeholder": "Enter your ingredients here.",
                    "rows": 4,
                    "cols": 20,
                }
            ),
            "instructions": Textarea(
                attrs={
                    "placeholder": "Enter your instructions here.",
                    "rows": 6,
                    "cols": 20,
                }
            ),
            "publish_date": TextInput(attrs={"placeholder": "DD/MM/YYYY"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "border-black rounded-0"
            self.fields[field].label = False
