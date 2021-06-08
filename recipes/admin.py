from django.contrib import admin
from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "publish_date",
        "featured_product",
    )


admin.site.register(Recipe, RecipeAdmin)
