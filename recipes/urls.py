from django.urls import path
from . import views


urlpatterns = [
    path("", views.all_recipes, name="recipes"),
    path("<str:recipe_title>/", views.recipe_detail, name="recipe_detail"),
]
