from django.shortcuts import render
from .models import Product


def all_products(request):
    """
    Returns page which contains all current products for the subscription
    service.
    """
    products = Product.objects.all()

    context = {"products": products}
    print(context["products"])
    return render(request, "products/products.html", context)
