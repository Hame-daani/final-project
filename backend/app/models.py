from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser


class Movie(models.Model):
    title = models.CharField(max_length=500)
    plot = models.CharField(max_length=500, blank=True)
    year = models.CharField(max_length=4, default="1900")
    imdbid = models.CharField(max_length=20, blank=True)
    tmdbid = models.CharField(max_length=20, blank=True)
    genres = ArrayField(models.CharField(max_length=10))
    poster = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.title


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    bio = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    friends = models.ManyToManyField("self")
    watchlist = models.ManyToManyField(Movie, related_name='watchlist')
    liked = models.ManyToManyField(Movie, related_name='liked')


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews',
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} [{self.movie.title}] - {self.rating}"


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('p', 'Pending'),
        ('a', 'Accepted'),
        ('r', 'Rejected')
    )
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='my_reqs')
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='to_me_reqs')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='p')
