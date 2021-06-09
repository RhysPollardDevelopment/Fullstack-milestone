from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404, reverse
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Recipe
from profiles.models import UserProfile
from .forms import RecipeForm


def is_superuser(user):
    if user.is_authenticated:
        if user.is_superuser:
            return True
        else:
            return False
    else:
        return False


def all_recipes(request):
    """
    Loads all recipes available at the moment for user to look through.
    """
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
    """
    Directs user to details page for each recipe, if user is anonymous or does
    not have an active subscription then as restricted variable is passed
    and content is blocked.

    Only last 3 months recipes are blocked.
    """
    recipe = get_object_or_404(Recipe, title=recipe_title)

    # https://stackoverflow.com/questions/3345030/splitting-a-string-separated
    # -by-r-n-into-a-list-of-lines/3345052
    # Use of splitlines to make textfiles easier to read.

    recipe.ingredients = recipe.ingredients.splitlines()

    recipe.instructions = recipe.instructions.splitlines()

    profile = None
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

    # Finds the date time 3 months prior to today
    three_months = datetime.now(tz=timezone.utc) + relativedelta(months=-3)

    # If recipe publish date is within last 3 months, is restricted to users
    # without subscriptions.
    if recipe.publish_date > three_months:
        # Requires check if authenticated to stop error on anonymous users.
        if request.user.is_authenticated and profile.has_active_subscription:
            restricted = False
        else:
            restricted = True
    else:
        restricted = False

    template = "recipes/recipe_detail.html"
    context = {"recipe": recipe, "restricted": restricted}
    return render(request, template, context)


@user_passes_test(is_superuser, login_url="/", redirect_field_name=None)
@login_required
def add_recipe(request):
    """
    Add a recipe to the database if user is a superuser.
    """

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save()
            messages.success(request, "Recipe added successfully!")
            return redirect(reverse("recipe_detail", args=[recipe.title]))
        else:
            messages.error(
                request,
                "Failed to create recipe. Please check form is correct.",
            )
    else:
        form = RecipeForm()

    context = {
        "form": form,
    }
    template = "recipes/add_recipe.html"
    return render(request, template, context)
