from django.db import models
from django.core.files.storage import default_storage

from core.models import TimeStampedUUIDModel, Address
from accounts.models import User


class Ustaz(TimeStampedUUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="ustaz")
    birth_date = models.DateField()
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

    def save(self, *args, **kwargs):
        if self._state.adding is False:
            old = Ustaz.objects.get(pk=self.pk)

            for field_name in [
                "nid_front",
                "nid_back",
                "guardian_permission_letter",
                "chairman_certificate",
                "pledge",
                "teacher_appreciation",
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
            "nid_front",
            "nid_back",
            "guardian_permission_letter",
            "chairman_certificate",
            "pledge",
            "teacher_appreciation",
        ]:
            file_field = getattr(self, field_name)
            if file_field and default_storage.exists(file_field.name):
                default_storage.delete(file_field.name)

        # remove related files if available
        for edu in self.education_qualification.all():
            edu.delete()

        for tr in self.training_certificates.all():
            tr.delete()

        for ac in self.achievement_certificates.all():
            ac.delete()

        for ot in self.organization_testimonials.all():
            ot.delete()

        super().delete(*args, **kwargs)



class EducationalQualification(TimeStampedUUIDModel):
    ustaz = models.ForeignKey(Ustaz, related_name='education_qualification', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def file_upload_path(instance, filename):
        return f"Ustaz-Educational-Qualification/{instance.ustaz.id}/{filename}"

    file = models.FileField(upload_to=file_upload_path, null=True, blank=True)

    class Meta:
        db_table = 'educational_qualifications'

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = EducationalQualification.objects.filter(pk=self.pk).first()
            old_file = old_instance.file if old_instance else None

            # File has been cleared
            if old_file and not self.file:
                if default_storage.exists(old_file.name):
                    default_storage.delete(old_file.name)

            # File has been replaced
            elif old_file and self.file and old_file.name != self.file.name:
                if default_storage.exists(old_file.name):
                    default_storage.delete(old_file.name)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print("delete called for deleting")
        if self.file and default_storage.exists(self.file.name):
            default_storage.delete(self.file.name)
        super().delete(*args, **kwargs)


class TrainingCertificate(TimeStampedUUIDModel):
    ustaz = models.ForeignKey(Ustaz, related_name='training_certificates', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def file_upload_path(instance, filename):
        return f"Ustaz-Training-Certificate/{instance.ustaz.id}/{filename}"

    file = models.FileField(upload_to=file_upload_path)

    class Meta:
        db_table = 'training_certificates'

    
    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = TrainingCertificate.objects.filter(pk=self.pk).first()
            old_file = old_instance.file if old_instance else None

            # File has been cleared
            if old_file and not self.file:
                if default_storage.exists(old_file.name):
                    default_storage.delete(old_file.name)

            # File has been replaced
            elif old_file and self.file and old_file.name != self.file.name:
                if default_storage.exists(old_file.name):
                    default_storage.delete(old_file.name)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file and default_storage.exists(self.file.name):
            default_storage.delete(self.file.name)
        super().delete(*args, **kwargs)


class AchievementCertificate(TimeStampedUUIDModel):
    ustaz = models.ForeignKey(Ustaz, related_name='achievement_certificates', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def file_upload_path(instance, filename):
        return f"Ustaz-Achievement-Certificate/{instance.ustaz.id}/{filename}"

    file = models.FileField(upload_to=file_upload_path)

    class Meta:
        db_table = 'achievement_certificates'

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = AchievementCertificate.objects.filter(pk=self.pk).first()
            old_file = old_instance.file if old_instance else None

            # File has been cleared
            if old_file and not self.file:
                if default_storage.exists(old_file.name):
                    default_storage.delete(old_file.name)

            # File has been replaced
            elif old_file and self.file and old_file.name != self.file.name:
                if default_storage.exists(old_file.name):
                    default_storage.delete(old_file.name)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file and default_storage.exists(self.file.name):
            default_storage.delete(self.file.name)
        super().delete(*args, **kwargs)


class OrganizationTestimonial(TimeStampedUUIDModel):
    ustaz = models.ForeignKey(Ustaz, related_name='organization_testimonials', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def file_upload_path(instance, filename):
        return f"Ustaz-Organization-Testimonial/{instance.ustaz.id}/{filename}"

    file = models.FileField(upload_to=file_upload_path)

    class Meta:
        db_table = 'organization_testimonials'

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = OrganizationTestimonial.objects.filter(pk=self.pk).first()
            old_file = old_instance.file if old_instance else None

            # File has been cleared
            if old_file and not self.file:
                if default_storage.exists(old_file.name):
                    default_storage.delete(old_file.name)

            # File has been replaced
            elif old_file and self.file and old_file.name != self.file.name:
                if default_storage.exists(old_file.name):
                    default_storage.delete(old_file.name)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file and default_storage.exists(self.file.name):
            default_storage.delete(self.file.name)
        super().delete(*args, **kwargs)

