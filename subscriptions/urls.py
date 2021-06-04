from django.urls import path
from . import views


urlpatterns = [
    path("", views.subscription_page, name="subscription_page"),
    path("checkout", views.checkout, name="checkout"),
    path("checkout/complete", views.complete, name="complete"),
    path(
        "create-subscription",
        views.create_subscription,
        name="create_subscription",
    ),
]
