from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Max

from core.models import Address, TimeStampedUUIDModel
from posts.choices import JobStatusChoices, JobTimeChoices, JobTypeChoices, UstazTypeChoices
from ustaz.models import Ustaz


class JobPost(TimeStampedUUIDModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.FloatField()
    job_time = models.CharField(max_length=50, choices=JobTimeChoices.choices, default=JobTimeChoices.PART_TIME)
    job_type = models.CharField(max_length=50, choices=JobTypeChoices.choices, default=JobTypeChoices.HOME_TUTORING)
    tuition_time = models.CharField(
        max_length=100,
        help_text="Expected teaching time, e.g. 'Mon-Thu, 5pm-7pm'",
        blank=True,
        null=True
    )
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=JobStatusChoices.choices, default=JobStatusChoices.DRAFTED)
    subjects = models.CharField(max_length=255)
    ustaz_type = models.CharField(max_length=10, choices=UstazTypeChoices.choices, default=UstazTypeChoices.ANY)

    # generic foreign key it can be for Organization, Guardian, or Student
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")
    is_verified = models.BooleanField(default=False)
    _job_number = models.BigIntegerField(unique=True, editable=False, null=True, db_column='job_number')

    class Meta:
        db_table = "job_posts"
        verbose_name = "Job Post"
        verbose_name_plural = "Job Posts"
        ordering = ["-created_at"]
    
    def save(self, *args, **kwargs):
        if self._job_number is None:
            last_number = JobPost.objects.aggregate(max_number=Max('_job_number'))['max_number'] or 0
            self._job_number = last_number + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content_object
    
    @property
    def job_number(self) -> str:
        return str(self._job_number).zfill(6) if self._job_number is not None else None

    @job_number.setter
    def job_number(self, value: str | int):
        self._job_number = int(value)


class UstazJobRequest(TimeStampedUUIDModel):
    ustaz = models.ForeignKey(Ustaz, on_delete=models.CASCADE, related_name="job_requests")
    title = models.CharField(max_length=255, help_text="Headline for your tuition offering")
    bio = models.TextField(help_text="Description about your experience, subject expertise, etc.")
    subjects = models.CharField(max_length=255, help_text="Comma-separated subjects (e.g. Math, English)")
    classes = models.CharField(max_length=255, help_text="Class levels you're interested in (e.g. 6-8, SSC)")
    status = models.CharField(max_length=50, choices=JobStatusChoices.choices, default=JobStatusChoices.DRAFTED)
    job_time = models.CharField(
        max_length=50,
        choices=JobTimeChoices.choices,
        default=JobTimeChoices.PART_TIME,
    )
    job_type = models.CharField(
        max_length=50,
        choices=JobTypeChoices.choices,
        default=JobTypeChoices.HOME_TUTORING,
    )
    tuition_time = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Preferred tuition time (e.g. Mon-Fri, 6-8 PM)",
    )
    expected_salary = models.FloatField(null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = "ustaz_job_requests"
        verbose_name = "Ustaz Job Post"
        verbose_name_plural = "Ustaz Job Posts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ustaz.user} - {self.title}"
