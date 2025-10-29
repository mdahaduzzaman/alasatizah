import uuid
from django.db import models
from django.core.files.storage import default_storage


class TimeStampedUUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Address(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=200)
    house = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.area}, {self.city}"

    class Meta:
        db_table = "addresses"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class JobType(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    ordering = models.PositiveIntegerField(default=0)

    def image_upload_path(instance, filename):
        return f"Job Types/{instance.pk}/{filename}"

    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "job_types"
        verbose_name = "Job Type"
        verbose_name_plural = "Job Types"
        ordering = ["ordering"]

    def save(self, *args, **kwargs):
        # Check if the instance already exists in the DB
        if self.pk:
            old_image = (
                self.__class__.objects.filter(pk=self.pk)
                .values_list("image", flat=True)
                .first()
            )
            if old_image and self.image and old_image != self.image.name:
                # Delete old image file
                if default_storage.exists(old_image):
                    default_storage.delete(old_image)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and default_storage.exists(self.image.name):
            default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class Testimonial(models.Model):
    class TypeChoices(models.TextChoices):
        STUDENT = "Student", "Student"
        GUARDIAN = "Guardian", "Guardian"
        ORGANIZATION = "Organization", "Organization"
        USTAZ = "Ustaz", "Ustaz"

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=15, choices=TypeChoices.choices, default=TypeChoices.STUDENT
    )
    ordering = models.PositiveIntegerField(default=0)

    def image_upload_path(instance, filename):
        return f"Testimonials/{instance.id}/{filename}"

    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "testimonials"
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def save(self, *args, **kwargs):
        # Check if the instance already exists in the DB
        if self.pk:
            old_image = (
                self.__class__.objects.filter(pk=self.pk)
                .values_list("image", flat=True)
                .first()
            )
            if old_image and self.image and old_image != self.image.name:
                # Delete old image file
                if default_storage.exists(old_image):
                    default_storage.delete(old_image)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and default_storage.exists(self.image.name):
            default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class JobCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    ordering = models.PositiveIntegerField(default=0)

    def image_upload_path(instance, filename):
        return f"JobCategory/{instance.id}/{filename}"

    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "job_categories"
        verbose_name = "Job Category"
        verbose_name_plural = "Job Categories"

    def save(self, *args, **kwargs):
        # Check if the instance already exists in the DB
        if self.pk:
            old_image = (
                self.__class__.objects.filter(pk=self.pk)
                .values_list("image", flat=True)
                .first()
            )
            if old_image and self.image and old_image != self.image.name:
                # Delete old image file
                if default_storage.exists(old_image):
                    default_storage.delete(old_image)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and default_storage.exists(self.image.name):
            default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)
