from django.db import models


class JobTimeChoices(models.TextChoices):
    ANY = "any", "Any"
    FULL_TIME = "full_time", "Full Time"
    PART_TIME = "part_time", "Part Time"


class JobStatusChoices(models.TextChoices):
    DRAFTED = "drafted", "Drafted"
    PUBLISHED = "published", "Published"
    CLOSED = "closed", "Closed"


class JobTypeChoices(models.TextChoices):
    ANY = "any", "Any"
    ONLINE = "online", "Online"
    HOME_TUTORING = "home_tutoring", "Home Tutoring"
    INSTITUTE = "institute", "At Institute"
    HYBRID = "hybrid", "Hybrid"


class UstazTypeChoices(models.TextChoices):
    ANY = "any", "Any"
    MALE = "male", "Male"
    FEMALE = "female", "Female"
