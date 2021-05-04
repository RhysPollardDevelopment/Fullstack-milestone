from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, Company


def all_products(request):
    """
    Returns page which contains all current products for the subscription
    service.
    """
    products = Product.objects.all()

    context = {"products": products}
    return render(request, "products/products.html", context)


def product_details(request, product_id):
    """
    Directs user to page for specific product, which contains details on
    product, link to owner company page and suggested recipes.
    """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)


def partners(request):
    """
    Opens a page containing a list of all companies in partnership with the
    main website.
    """
    companies = Company.objects.all()
    context = {"companies": companies}

    return render(request, "products/partners.html", context)
