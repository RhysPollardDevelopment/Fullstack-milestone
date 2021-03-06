from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404, reverse
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required, user_passes_test
import random

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
    recipes = list(
        Recipe.objects.filter(publish_date__lte=now).order_by("-publish_date")
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

    # If recipe publish date is within last 3 months, is restricted to users
    # without subscriptions.
    if recipe.is_restricted:
        # Requires check if authenticated to stop error on anonymous users.
        if request.user.is_authenticated and profile.has_active_subscription:
            restricted = False
        else:
            restricted = True
    else:
        restricted = False

    now = datetime.now(tz=timezone.utc)

    other_recipes = list(
        Recipe.objects.filter(publish_date__lte=now).exclude(id=recipe.id)
    )
    # If statement to defend against unlikely instance of less than four
    # recipes. Also assign to none if empty to allow prepared message.
    if len(other_recipes) > 3:
        recipes = random.sample((other_recipes), 4)
    elif len(other_recipes) == 0:
        recipes = None
    else:
        recipes = other_recipes

    template = "recipes/recipe_detail.html"
    context = {
        "recipe": recipe,
        "restricted": restricted,
        "recipes": recipes,
    }
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


@user_passes_test(is_superuser, login_url="/", redirect_field_name=None)
@login_required
def update_recipe(request, recipe_title):
    """
    Edit a recipe retrieved from the database if user is a superuser.
    """
    recipe = get_object_or_404(Recipe, title=recipe_title)

    # If method is post, load the form with data, files and model instance.
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        # If valid, save the model instance and redirect to updated page.
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe updated successfully!")
            return redirect(reverse("recipe_detail", args=[recipe.title]))
        else:
            messages.error(
                request,
                "An error was found. Please check form is correct.",
            )
    #  Method is get, fill form with stored information.
    else:
        form = RecipeForm(instance=recipe)

    context = {
        "recipe": recipe,
        "form": form,
    }
    template = "recipes/update_recipe.html"
    return render(request, template, context)


@user_passes_test(is_superuser, login_url="/", redirect_field_name=None)
@login_required
def delete_recipe(request, recipe_title):
    """Delete a recipe from the database."""
    recipe = get_object_or_404(Recipe, title=recipe_title)
    recipe.delete()
    messages.success(request, "Recipe deleted successfully.")
    return redirect(reverse("recipes"))
