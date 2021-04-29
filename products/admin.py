from django.contrib import admin
from .models import Product, Company


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "image",
        "texture",
        "flavour",
        "company",
    )


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "logo",
        "county",
        "company_url",
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Company, CompanyAdmin)
