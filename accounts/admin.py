from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from accounts.models import User
from accounts.forms import UserCreationForm


@admin.register(User)
class UserModelAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ["name", "email", "is_active", "is_staff", "is_superuser"]
    list_filter = ("is_active", "is_staff", "is_superuser", "roles")
    readonly_fields = ["id", "created_at", "updated_at", "last_login"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "phone", "gender", "avatar")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "roles",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Additional Info",
            {"fields": ("id", "created_at", "updated_at", "last_login")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "phone",
                    "gender",
                    "avatar",
                    "roles",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email", "name")
    ordering = ["-created_at"]
