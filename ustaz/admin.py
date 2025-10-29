from django.contrib import admin


from ustaz.models import (
    Ustaz,
    AchievementCertificate,
    EducationalQualification,
    TrainingCertificate,
)


class EducationalQualificationInline(admin.TabularInline):
    model = EducationalQualification
    extra = 0
    fields = ["file", "is_verified"]
    readonly_fields = []


class AchievementCertificateInline(admin.TabularInline):
    model = AchievementCertificate
    extra = 0
    fields = ["file", "is_verified"]
    readonly_fields = []


class TrainingCertificateInline(admin.TabularInline):
    model = TrainingCertificate
    extra = 0
    fields = ["file", "is_verified"]
    readonly_fields = []


@admin.register(Ustaz)
class UstazModelAdmin(admin.ModelAdmin):
    inlines = [
        EducationalQualificationInline,
        AchievementCertificateInline,
        TrainingCertificateInline,
    ]
    list_display = ["user", "birth_date", "nid_no", "is_verified"]
    search_fields = ["user__name", "user__email"]
    list_filter = ["is_verified"]
    readonly_fields = ["id", "created_at", "updated_at"]
