from django.dispatch import receiver
from django.db.models.signals import post_migrate

from accounts.models import Role


@receiver(post_migrate)
def create_initial_roles(sender, **kwargs):
    """signal to create initial roles on migrations"""
    if sender.name == "accounts":
        roles = ["ustaz", "organization"]
        Role.objects.bulk_create([Role(name=role_name) for role_name in roles])
        print("initial roles created")
