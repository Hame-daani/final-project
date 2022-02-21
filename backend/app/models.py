from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=4, default="1900")
    imdbid = models.CharField(max_length=20, blank=True)
    tmdbid = models.CharField(max_length=20, blank=True)
    genres = ArrayField(models.CharField(max_length=10))


class User(AbstractUser):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    )
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    friends = models.ManyToManyField("self")
    watchlist = models.ManyToManyField(Movie, related_name='watchlist')
    liked = models.ManyToManyField(Movie, related_name='liked')
