from django.db import models
from django.core.files.storage import default_storage
from django.contrib.contenttypes.fields import GenericRelation

from accounts.models import User
from core.models import TimeStampedUUIDModel, Address
from posts.models import JobPost


class Organization(TimeStampedUUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="organization")
    name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=100, null=True, blank=True)
    facebook_page = models.URLField(max_length=200, null=True, blank=True)
    youtube_page = models.URLField(max_length=200, null=True, blank=True)
    head_name = models.CharField(max_length=100)

    def nid_upload_path(instance, filename):
        return f"Organization-Head-NID-{instance.id}/{filename}"
    
    def ha_upload_path(instance, filename):
        return f"Organization-Head-Avatar/{instance.id}/{filename}"
    
    def ta_upload_path(instance, filename):
        return f"Organization-Teacher-Accomodation/{instance.id}/{filename}"
    
    def mr_upload_path(instance, filename):
        return f"Organization-Meal-Routine/{instance.id}/{filename}"
    
    def hc_upload_path(instance, filename):
        return f"Organization-Holiday-Calender/{instance.id}/{filename}"
    
    def cp_upload_path(instance, filename):
        return f"Organization-Committe-Permission/{instance.id}/{filename}"
    
    def pledge_upload_path(instance, filename):
        return f"Organization-Pledge/{instance.id}/{filename}"
    
    head_nid = models.FileField(upload_to=nid_upload_path, null=True, blank=True)
    head_avatar = models.ImageField(upload_to=ha_upload_path, null=True, blank=True)
    teacher_accomodation = models.ImageField(upload_to=ta_upload_path, null=True, blank=True)
    meal_routine = models.ImageField(upload_to=mr_upload_path, null=True, blank=True)
    hoilday_calendar = models.ImageField(upload_to=hc_upload_path, null=True, blank=True)
    rules = models.TextField(null=True, blank=True)
    committee_permission = models.ImageField(upload_to=cp_upload_path, null=True, blank=True)
    pledge = models.ImageField(upload_to=pledge_upload_path, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    job_posts = GenericRelation(JobPost, related_query_name='guardian')

    class Meta:
        db_table = 'organizations'
        managed = True
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def save(self, *args, **kwargs):
        if self._state.adding is False:
            old = Organization.objects.get(pk=self.pk)

            for field_name in [
                "head_nid",
                "head_avatar",
                "teacher_accomodation",
                "meal_routine",
                "hoilday_calendar",
                "committee_permission",
                "pledge",
            ]:
                old_file = getattr(old, field_name)
                new_file = getattr(self, field_name)

                # File has been cleared or replaced
                if old_file and (not new_file or old_file.name != new_file.name):
                    if default_storage.exists(old_file.name):
                        default_storage.delete(old_file.name)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for field_name in [
            "head_nid",
            "head_avatar",
            "teacher_accomodation",
            "meal_routine",
            "hoilday_calendar",
            "committee_permission",
            "pledge",
        ]:
            file_field = getattr(self, field_name)
            if file_field and default_storage.exists(file_field.name):
                default_storage.delete(file_field.name)

        super().delete(*args, **kwargs)