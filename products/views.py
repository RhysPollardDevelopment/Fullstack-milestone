from django.shortcuts import render


def all_products(request):

    return render(request, "products/products.html")
