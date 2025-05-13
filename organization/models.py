from django.db import models

from accounts.models import User
from core.models import TimeStampedUUIDModel, Address


class Organization(TimeStampedUUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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