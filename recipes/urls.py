from django.urls import path
from . import views


urlpatterns = [
    path("", views.all_recipes, name="recipes"),
    path("add/", views.add_recipe, name="add_recipe"),
    path(
        "recipe/<str:recipe_title>/", views.recipe_detail, name="recipe_detail"
    ),
]
