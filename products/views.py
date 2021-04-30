from django.shortcuts import render
from .models import Product


def all_products(request):
    product = Product.objects.create(name="named", description="description")
    str(product)
    return render(request, "products/products.html")
