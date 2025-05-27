from django.db import models
from django.contrib.contenttypes.fields import GenericRelation


from accounts.models import User
from core.models import Address, TimeStampedUUIDModel
from posts.models import JobPost


class Guardian(TimeStampedUUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guardian')
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    is_verified = models.BooleanField(default=False)
    job_posts = GenericRelation(JobPost, related_query_name='guardian')

    class Meta:
        db_table = 'guardians'
        verbose_name = 'Guardian'
        verbose_name_plural = 'Guardians'

    def __str__(self):
        return self.user.name