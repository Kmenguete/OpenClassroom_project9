from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    SUBSCRIPTION = 'SUBSCRIPTION'
    ROLE_CHOICES = (
        (SUBSCRIPTION, 'SUBSCRIPTION'),
    )
    profile_photo = models.ImageField(verbose_name='profile picture')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name='Role', null=True)
