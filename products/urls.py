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
    path("partners/", views.partners, name="partners"),
    path("partners/add_company/", views.add_company, name="add_company"),
    path(
        "partners/update_company/<int:company_id>/",
        views.update_company,
        name="update_company",
    ),
    path(
        "partners/delete_company/<int:company_id>/",
        views.delete_company,
        name="delete_company",
    ),
    path("<int:product_id>/", views.product_details, name="product_details"),
]
