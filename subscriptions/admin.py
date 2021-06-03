from django.contrib import admin
from .models import Subscription, StripeSubscription, Invoice


class Subscription_Admin(admin.ModelAdmin):
    list_display = (
        "user_profile",
        "start_date",
        "expiry_date",
        "cancel_date",
    )


class StripeSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "subscription_id",
        "start_date",
        "end_date",
        "stripe_user",
    )


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "stripe_subscription",
        "invoice_number",
        "current_start",
        "current_end",
    )


admin.site.register(Subscription, Subscription_Admin)
admin.site.register(StripeSubscription, StripeSubscriptionAdmin)
admin.site.register(Invoice, InvoiceAdmin)
