from django.urls import path
from . import views


urlpatterns = [
    path("", views.profiles, name="profiles"),
    path("update_address/", views.update_address, name="update_address"),
    path(
        "password_change_done",
        views.password_change_done,
        name="password_change_done",
    ),
    path("my_recipes/", views.my_recipes, name="my_recipes"),
    path(
        "subscription_history/",
        views.subscription_history,
        name="subscription_history",
    ),
]
