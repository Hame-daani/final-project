from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    )
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
