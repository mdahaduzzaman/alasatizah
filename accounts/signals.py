from django.dispatch import receiver
from django.db.models.signals import post_migrate

from accounts.models import Role


@receiver(post_migrate)
def create_initial_roles(sender, **kwargs):
    """Signal to create initial roles on migrations."""
    if sender.name == "accounts":
        roles = ["ustaz", "organization", "guardian"]
        for role_name in roles:
            Role.objects.get_or_create(name=role_name)
        print("Initial roles ensured (created if not exist).")
