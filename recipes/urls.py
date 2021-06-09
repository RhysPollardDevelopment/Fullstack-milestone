from django.urls import path
from . import views


urlpatterns = [
    path("", views.all_recipes, name="recipes"),
    path("add_recipe/", views.add_recipe, name="add_recipe"),
    path(
        "update_recipe/<str:recipe_title>/",
        views.update_recipe,
        name="update_recipe",
    ),
    path(
        "delete_recipe/<str:recipe_title>/",
        views.delete_recipe,
        name="delete_recipe",
    ),
    path(
        "recipe/<str:recipe_title>/", views.recipe_detail, name="recipe_detail"
    ),
]
