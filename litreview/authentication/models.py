from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REVIEWER = 'REVIEWER'
    REVIEW_ASKER = 'REVIEW_ASKER'
    ROLE_CHOICES = (
        (REVIEWER, 'Reviewer'),
        (REVIEW_ASKER, 'Review_asker'),
    )
    profile_photo = models.ImageField(verbose_name='profile picture')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name='Role', null=True)
