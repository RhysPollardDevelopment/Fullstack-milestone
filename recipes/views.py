from django.shortcuts import render, get_object_or_404
from .models import Recipe
from datetime import datetime, timezone


def all_recipes(request):
    recipes = Recipe.objects.filter(
        publish_date__lte=datetime.now(tz=timezone.utc)
    )

    template = "recipes/recipes.html"
    context = {"recipes": recipes}
    return render(request, template, context)


def recipe_detail(request, recipe_title):
    print(recipe_title)
    recipe = get_object_or_404(Recipe, title=recipe_title)

    template = "recipes/recipe_detail.html"
    context = {"recipe": recipe}
    return render(request, template, context)
