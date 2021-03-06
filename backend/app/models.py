from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from recommender.models import Similarity

genres = [
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Fantasy",
    "Romance",
    "Drama",
    "Action",
    "Crime",
    "Thriller",
    "Horror",
    "Mystery",
    "Sci-Fi",
    "IMAX",
    "Documentar",
    "War",
    "Musical",
    "Western",
    "Film-Noir",
]


class Median(models.Aggregate):
    function = "PERCENTILE_CONT"
    name = "median"
    output_field = models.FloatField()
    template = "%(function)s(0.5) WITHIN GROUP (ORDER BY %(expressions)s)"


class User(AbstractUser):
    def avatar_upload_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
        return f"avatars/user_avatar_{instance.id}"

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    bio = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(
        upload_to=avatar_upload_path, default="avatars/default_avatar.png"
    )
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    similarities = GenericRelation(Similarity, object_id_field="source_id")


class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "content_type", "object_id"]

    def __str__(self) -> str:
        return f"{self.user.first_name} liked this {self.content_type.model} {self.object_id}"


class Movie(models.Model):
    title = models.CharField(max_length=500)
    plot = models.TextField(blank=True)
    year = models.CharField(max_length=4, default="1900")
    imdbid = models.CharField(max_length=20, blank=True)
    tmdbid = models.CharField(max_length=20, blank=True)
    genres = ArrayField(models.CharField(max_length=10))
    poster = models.URLField(blank=True)
    similarities = GenericRelation(Similarity, object_id_field="source_id")
    watchlist = models.ManyToManyField(User, related_name="watchlist")
    likes = GenericRelation(Like)

    @property
    def avg_rating(self):
        movie_ratings = Movie.objects.annotate(rcount=models.Count("reviews"))
        c = Review.objects.aggregate(avg=models.Avg("rating"))["avg"]
        m = movie_ratings.aggregate(m=Median("rcount"))["m"]
        v = movie_ratings.get(id=self.id).rcount
        r = Review.objects.filter(movie=self.id).aggregate(avg=models.Avg("rating"))[
            "avg"
        ]
        try:
            return (v / (v + m) * r) + (m / (m + v) * c)
        except:
            return 0

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    comments = GenericRelation("self")
    likes = GenericRelation(Like)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} on this {self.content_type.model}:{self.object_id} says {self.text}"


class Review(models.Model):
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)

    class Meta:
        unique_together = ["user", "movie"]

    def __str__(self) -> str:
        return f"{self.user.first_name} [{self.movie.title}] - {self.rating}"


class FriendRequest(models.Model):
    STATUS_CHOICES = (("p", "Pending"), ("a", "Accepted"), ("r", "Rejected"))
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_reqs"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="to_me_reqs"
    )
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="p")

    def __str__(self) -> str:
        return f"{self.from_user.get_full_name()} wants to be {self.to_user.get_full_name()} friends"
