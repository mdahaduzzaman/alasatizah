from django.db import models

from core.models import TimeStampedUUIDModel, Address
from accounts.models import User


class Ustaz(TimeStampedUUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="ustaz")
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    nid_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    birth_certificate_no = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def nid_front_upload_path(instance, filename):
        return f"Ustaz-NID-Front/{instance.id}/{filename}"
    
    def nid_back_upload_path(instance, filename):
        return f"Ustaz-NID-Back/{instance.id}/{filename}"
    
    def gpl_upload_path(instance, filename):
        return f"Ustaz-Guardian-Permission/{instance.id}/{filename}"
    
    def cc_upload_path(instance, filename):
        return f"Ustaz-Chairman-Certificate/{instance.id}/{filename}"
    
    def pledge_upload_path(instance, filename):
        return f"Ustaz-Pledge/{instance.id}/{filename}"
    
    def ta_upload_path(instance, filename):
        return f"Ustaz-Teacher-Appreciation/{instance.id}/{filename}"
    
    nid_front = models.ImageField(upload_to=nid_front_upload_path, null=True, blank=True)
    nid_back = models.ImageField(upload_to=nid_back_upload_path, null=True, blank=True)
    guardian_permission_letter = models.FileField(upload_to=gpl_upload_path, null=True, blank=True)
    chairman_certificate = models.FileField(upload_to=cc_upload_path, null=True, blank=True)
    pledge = models.FileField(upload_to=pledge_upload_path, null=True, blank=True)
    teacher_appreciation = models.FileField(upload_to=ta_upload_path, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = 'asatizah'
        verbose_name = 'Uztaz'
        verbose_name_plural = 'Asatizah'


class EducationalQualification(TimeStampedUUIDModel):
    ustaz = models.ForeignKey(Ustaz, related_name='educations', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def file_upload_path(instance, filename):
        return f"Ustaz-Educational-Qualification/{instance.ustaz.id}/{filename}"

    file = models.FileField(upload_to=file_upload_path, null=True, blank=True)

    class Meta:
        db_table = 'educational_qualifications'


class TrainingCertificate(TimeStampedUUIDModel):
    ustaz = models.ForeignKey(Ustaz, related_name='training_certificates', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def file_upload_path(instance, filename):
        return f"Ustaz-Training-Certificate/{instance.ustaz.id}/{filename}"

    file = models.FileField(upload_to=file_upload_path)

    class Meta:
        db_table = 'training_certificates'


class AchievementCertificate(TimeStampedUUIDModel):
    ustaz = models.ForeignKey(Ustaz, related_name='achievement_certificates', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def file_upload_path(instance, filename):
        return f"Ustaz-Achievement-Certificate/{instance.ustaz.id}/{filename}"

    file = models.FileField(upload_to=file_upload_path)

    class Meta:
        db_table = 'achievement_certificates'


class OrganizationTestimonial(TimeStampedUUIDModel):
    ustaz = models.ForeignKey(Ustaz, related_name='organization_testimonials', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def file_upload_path(instance, filename):
        return f"Ustaz-Organization-Testimonial/{instance.ustaz.id}/{filename}"

    file = models.FileField(upload_to=file_upload_path)

    class Meta:
        db_table = 'organization_testimonials'

