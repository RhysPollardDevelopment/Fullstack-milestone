from django.contrib import admin
from .models import StripeSubscription, Invoice


class StripeSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "subscription_id",
        "start_date",
        "end_date",
        "stripe_user",
    )
    # https://docs.djangoproject.com/en/dev/topics/db/queries/
    # #lookups-that-span-relationships - for foreignkey filter.
    search_fields = [
        "stripe_user__user__username",
    ]


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "stripe_subscription",
        "invoice_number",
        "current_start",
        "current_end",
    )
    search_fields = [
        "stripe_subscription__subscription_id",
    ]


admin.site.register(StripeSubscription, StripeSubscriptionAdmin)
admin.site.register(Invoice, InvoiceAdmin)
