from django.shortcuts import render, get_object_or_404
from .models import Recipe
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from profiles.models import UserProfile


def all_recipes(request):
    now = datetime.now(tz=timezone.utc)
    # Retrieve all recipes with publish dates before today and order them
    # in descending order.
    recipes = Recipe.objects.filter(publish_date__lte=now).order_by(
        "-publish_date"
    )

    template = "recipes/recipes.html"
    context = {"recipes": recipes}
    return render(request, template, context)


def recipe_detail(request, recipe_title):
    recipe = get_object_or_404(Recipe, title=recipe_title)
    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

    # Finds the date time 3 months prior to this point
    three_months = datetime.now(tz=timezone.utc) + relativedelta(months=-3)

    if recipe.publish_date > three_months:
        if request.user.is_authenticated and profile.has_active_subscription:
            restricted = False
        else:
            restricted = True
    else:
        restricted = False

    template = "recipes/recipe_detail.html"
    context = {"recipe": recipe, "restricted": restricted}
    return render(request, template, context)
