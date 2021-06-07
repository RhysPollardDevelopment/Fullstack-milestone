from django.contrib import admin
import stripe
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


admin.site.register(Subscription, Subscription_Admin)
admin.site.register(StripeSubscription, StripeSubscriptionAdmin)
admin.site.register(Invoice, InvoiceAdmin)
