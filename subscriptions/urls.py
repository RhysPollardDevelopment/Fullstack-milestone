from django.urls import path
from . import views
from .webhooks import webhook_received


urlpatterns = [
    path("", views.subscription_page, name="subscription_page"),
    path("checkout", views.checkout, name="checkout"),
    path("checkout/complete", views.complete, name="complete"),
    path(
        "create-subscription",
        views.create_subscription,
        name="create_subscription",
    ),
    path("webhook/", webhook_received, name="webhook_received"),
]
