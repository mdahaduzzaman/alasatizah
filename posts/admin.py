from django.contrib import admin

from posts.models import JobPost, UstazJobRequest


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = (
        "get_owner",
        "get_owner_type",
        "job_time",
        "status",
        "job_type",
        "ustaz_type",
        "salary",
        "deadline",
        "is_verified",
    )
    search_fields = ("title", "subjects")
    ordering = ("-created_at",)

    def get_owner(self, obj: JobPost):
        return str(obj.content_object)

    def get_owner_type(self, obj: JobPost):
        return "Guardian/Student" if obj.content_type.model == "guardian" else "Organization"

    get_owner.short_description = "Owner"

    get_owner_type.short_description = "Owner Type"


@admin.register(UstazJobRequest)
class UstazJobRequestAdmin(admin.ModelAdmin):
    list_display = (
        "ustaz",
        "status",
        "is_verified",
        "expected_salary",
    )
    search_fields = ("ustaz__name", "ustaz__email")
    ordering = ("-created_at",)

