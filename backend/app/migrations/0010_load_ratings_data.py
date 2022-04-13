from django.db import migrations, models
import pandas as pd
from datetime import datetime
from django.utils.timezone import make_aware
from app.utils import timed
from tqdm import tqdm


@timed
def add_ratings(apps, schema):
    df = pd.read_csv("data/ratings.csv", low_memory=False)
    Review = apps.get_model("app", "Review")

    cache = []
    cache_size = 1000
    counter = 0
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        userid = row["userId"]
        movieid = row["movieId"]
        rating = row["rating"]
        timestamp = row["timestamp"]
        date = make_aware(datetime.fromtimestamp(timestamp))
        text = row["text"]
        cache.append(
            Review(
                user_id=userid,
                movie_id=movieid,
                text=text,
                rating=int(float(rating) * 2),
                created_at=date,
                updated_at=date,
            )
        )
        counter += 1
        if counter % cache_size == 0:
            Review.objects.bulk_create(cache)
            del cache
            cache = []
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
