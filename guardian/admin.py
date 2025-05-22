from django.contrib import admin

from guardian.models import Guardian


@admin.register(Guardian)
class GuardianModelAdmin(admin.ModelAdmin):
    list_display = ["user", "is_verified"]
    search_fields = ["user__name", "user__email"]
    list_filter = ["is_verified"]