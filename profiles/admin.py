from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "stripe_customer_id", "default_phone_number")


admin.site.register(UserProfile, UserProfileAdmin)
