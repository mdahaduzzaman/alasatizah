from django.contrib import admin

from organization.models import Organization


@admin.register(Organization)
class OrganizationModelAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "email", "is_verified"]
    search_fields = ["user__name", "user__email"]
    list_filter = ["is_verified"]
