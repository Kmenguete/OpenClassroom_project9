from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    SUBSCRIBER = 'SUBSCRIBER'
    ROLE_CHOICES = (
        (SUBSCRIBER, 'SUBSCRIBER'),
    )
    profile_photo = models.ImageField(verbose_name='profile picture')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name='Role', null=True)

    def __str__(self):
        return self.username
