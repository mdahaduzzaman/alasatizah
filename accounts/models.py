from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.core.validators import MinLengthValidator
from django.core.files.storage import default_storage

from accounts.choices import GenderChoices
from accounts.managers import UserManager
from core.models import TimeStampedUUIDModel


class Role(Group):
    class Meta:
        proxy = True
        verbose_name = "Role"
        verbose_name_plural = "Roles"


class User(AbstractBaseUser, PermissionsMixin, TimeStampedUUIDModel):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(10)],
        null=True,
        blank=True,
    )
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role, related_name="users", blank=True)
    is_deleted = models.BooleanField(default=False)

    def avatar_upload_path(instance, filename):
        return f"Avatar/{instance.email}/{filename}"

    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name

    class Meta:
        db_table = "users"

    def save(self, *args, **kwargs):
        # Check if the instance already exists in the DB
        if self.pk:
            old_avatar = (
                self.__class__.objects.filter(pk=self.pk)
                .values_list("avatar", flat=True)
                .first()
            )
            if old_avatar and self.avatar and old_avatar != self.avatar.name:
                # Delete old avatar file
                if default_storage.exists(old_avatar):
                    default_storage.delete(old_avatar)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.avatar and default_storage.exists(self.avatar.name):
            default_storage.delete(self.avatar.name)
        super().delete(*args, **kwargs)
