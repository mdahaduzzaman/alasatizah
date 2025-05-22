from django.core.management.base import BaseCommand

from accounts.choices import GenderChoices
from accounts.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            email="admin@alasatizah.com",
            defaults={
                "name": "Mr Admin",
                "gender":  GenderChoices.MALE,
                "is_active": True,
                "is_staff": True,
                "is_superuser": True
            }
        )
        if created:
            user.set_password("admin")
            user.save()