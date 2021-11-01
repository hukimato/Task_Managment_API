from django.contrib import admin
from .models import User


@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    """Профиль пользователя"""
    list_display = ("username", "last_name", "first_name", "email", "is_staff")
    list_display_links = ("username",)
    list_editable = ("is_staff",)

    fieldsets = (
        (None, {
            "fields": (("email", "username", "password"),)
        }),
        (None, {
            "fields": (("last_name", "first_name"),)
        })
    )

    def get_user(self, obj):
        return obj.user.email

    get_user.short_description = "Пользователь"
