from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Product, Company
from .forms import ProductForm, CompanyForm
from django.contrib.auth.decorators import login_required, user_passes_test
from recipes.views import is_superuser


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


@user_passes_test(is_superuser, login_url="/", redirect_field_name=None)
@login_required
def add_product(request):
    """
    Add a product to the database if user is a superuser.
    """

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save()
            messages.success(request, "product added successfully!")
            return redirect(reverse("product_details", args=[product.id]))
        else:
            messages.error(
                request,
                "Failed to create product. Please check form is correct.",
            )
    else:
        form = ProductForm()

    context = {
        "form": form,
    }
    template = "products/add_product.html"
    return render(request, template, context)


@user_passes_test(is_superuser, login_url="/", redirect_field_name=None)
@login_required
def update_product(request, product_id):
    """
    Edit a product retrieved from the database if user is a superuser.
    """
    product = get_object_or_404(Product, pk=product_id)

    # If method is post, load the form with data, files and model instance.
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        # If valid, save the model instance and redirect to updated page.
        if form.is_valid():
            form.save()
            messages.success(request, "product updated successfully!")
            return redirect(reverse("product_details", args=[product.id]))
        else:
            messages.error(
                request,
                "An error was found. Please check form is correct.",
            )
    #  Method is get, fill form with stored information.
    else:
        form = ProductForm(instance=product)

    context = {
        "product": product,
        "form": form,
    }
    template = "products/update_product.html"
    return render(request, template, context)


@user_passes_test(is_superuser, login_url="/", redirect_field_name=None)
@login_required
def delete_product(request, product_id):
    """Delete a product from the database."""
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, "product deleted successfully.")
    return redirect(reverse("products"))
