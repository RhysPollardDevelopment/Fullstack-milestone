from django.urls import path
from . import views


urlpatterns = [
    path("", views.all_products, name="products"),
    path("add_product/", views.add_product, name="add_product"),
    path(
        "update_product/<int:product_id>/",
        views.update_product,
        name="update_product",
    ),
    path(
        "delete_product/<int:product_id>/",
        views.delete_product,
        name="delete_product",
    ),
    path("<int:product_id>/", views.product_details, name="product_details"),
    path("partners/", views.partners, name="partners"),
]
