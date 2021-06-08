from django.shortcuts import render
from .models import Recipe
from datetime import datetime, timezone


def all_recipes(request):
    recipes = Recipe.objects.filter(
        publish_date__lte=datetime.now(tz=timezone.utc)
    )

    template = "recipes/recipes.html"
    context = {"recipes": recipes}
    return render(request, template, context)


def recipe_detail(request):
    template = "recipes/recipe_detail.html"
    return render(request, template)
