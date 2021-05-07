from django.contrib import admin
from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user_profile",
        "start_date",
        "expiry_date",
    )


admin.site.register(Subscription, SubscriptionAdmin)
