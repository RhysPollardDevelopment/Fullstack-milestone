from django.urls import path
from . import views


urlpatterns = [
    path("", views.profiles, name="profiles"),
    path("update_address/", views.update_address, name="update_address"),
    # path("partners/", views.partners, name="partners"),
]
