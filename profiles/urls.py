from django.urls import path
from . import views


urlpatterns = [
    path("", views.all_products, name="profiles"),
    # path("partners/", views.partners, name="partners"),
]
