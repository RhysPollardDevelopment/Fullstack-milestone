from django.urls import path
from . import views


urlpatterns = [
    path("", views.subscription_page, name="subscription_page"),
]
