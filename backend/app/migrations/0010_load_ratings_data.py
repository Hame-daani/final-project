from django.db import migrations, models
import pandas as pd
from datetime import datetime
from django.utils.timezone import make_aware
from app.utils import timed


@timed
def add_ratings(apps, schema):
    df = pd.read_csv("data/ratings.csv", low_memory=False)
    Review = apps.get_model("app", "Review")
    Movie = apps.get_model("app", "Movie")
    User = apps.get_model("app", "User")
    cache = []
    counter = 0
    print(f"{df.shape[0]} rating will be added")
    for index, row in df.iterrows():
        userid = row["userId"]
        movieid = row["movieId"]
        user = User.objects.get(id=userid)
        movie = Movie.objects.get(id=movieid)
        rating = row["rating"]
        timestamp = row["timestamp"]
        date = make_aware(datetime.fromtimestamp(timestamp))
        text = row["text"]
        cache.append(
            Review(
                user=user,
                movie=movie,
                text=text,
                rating=int(float(rating) * 2),
                created_at=date,
                updated_at=date,
            )
        )
        counter += 1
        if counter % 1000 == 0:
            Review.objects.bulk_create(cache)
            cache = []
            print(f"{counter} ratings added", end="\r")
    Review.objects.bulk_create(cache)


@timed
def removing_ratings(apps, schema):
    Review = apps.get_model("app", "Review")
    Review.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_load_users_extra_data"),
    ]

    operations = [
        migrations.RunPython(
            add_ratings,
            reverse_code=removing_ratings,
        ),
        migrations.operations.AlterField(
            model_name="review",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.operations.AlterField(
            model_name="review",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
