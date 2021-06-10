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
            messages.success(request, "Product added successfully!")
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
            messages.success(request, "Product updated successfully!")
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
    messages.success(request, "Product deleted successfully.")
    return redirect(reverse("products"))


# Company CRUD views.


@user_passes_test(is_superuser, login_url="/", redirect_field_name=None)
@login_required
def add_company(request):
    """
    Add a company to the database if user is a superuser.
    """

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Company added successfully!")
            return redirect(reverse("partners"))
        else:
            messages.error(
                request,
                "Failed to create company. Please check form is correct.",
            )
    else:
        form = CompanyForm()

    context = {
        "form": form,
    }
    template = "products/add_company.html"
    return render(request, template, context)


@user_passes_test(is_superuser, login_url="/", redirect_field_name=None)
@login_required
def update_company(request, company_id):
    """
    Edit a company retrieved from the database if user is a superuser.
    """
    company = get_object_or_404(Company, pk=company_id)

    # If method is post, load the form with data, files and model instance.
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)

        # If valid, save the model instance and redirect to updated page.
        if form.is_valid():
            form.save()
            messages.success(request, "Company updated successfully!")
            return redirect(reverse("partners"))
        else:
            messages.error(
                request,
                "An error was found. Please check form is correct.",
            )
    #  Method is get, fill form with stored information.
    else:
        form = CompanyForm(instance=company)

    context = {
        "company": company,
        "form": form,
    }
    template = "products/update_company.html"
    return render(request, template, context)


@user_passes_test(is_superuser, login_url="/", redirect_field_name=None)
@login_required
def delete_company(request, company_id):
    """Delete a company from the database."""
    company = get_object_or_404(Company, pk=company_id)
    company.delete()
    messages.success(request, "Company deleted successfully.")
    return redirect(reverse("partners"))
