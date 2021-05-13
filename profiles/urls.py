from django.urls import path
from . import views


urlpatterns = [
    path("", views.profiles, name="profiles"),
    # path("partners/", views.partners, name="partners"),
]
