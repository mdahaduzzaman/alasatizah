from django.contrib import admin

from core.models import JobCategory, JobType, Testimonial

admin.site.site_header = "Alasatizah Admin"
admin.site.site_title = "Admin"
admin.site.index_title = "Welcome to Alasatizah Admin Dashboard"


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ("ordering", "title", "image")
    search_fields = ("title", "description")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("ordering", "name", "position", "type", "image")
    search_fields = ("name", "position", "description")
    ordering = ["type", "ordering"]


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("ordering", "title", "image")
    search_fields = ("title", "image__name")
    ordering = ["ordering"]
