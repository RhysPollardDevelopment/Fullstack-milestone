from django.urls import path
from . import views


urlpatterns = [
    path("", views.profiles, name="profiles"),
    path("update/address/", views.update_address, name="update_address"),
    path("update/billing/", views.update_billing, name="update_billing"),
    path(
        "password_change_done",
        views.password_change_done,
        name="password_change_done",
    ),
    path(
        "subscription_history/",
        views.subscription_history,
        name="subscription_history",
    ),
]
