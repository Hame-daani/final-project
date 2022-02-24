from django.db import migrations
import pandas as pd
from datetime import datetime
from app.utils import timed


@timed
def add_ratings(apps, schema):
    df = pd.read_csv('data/ratings_clean.csv', low_memory=False)
    Review = apps.get_model('app', 'Review')
    Movie = apps.get_model('app', 'Movie')
    User = apps.get_model('app', 'User')
    for index, row in df.iterrows():
        userid = row['userId']
        movieid = row['movieId']
        user = User.objects.get(id=userid)
        movie = Movie.objects.get(id=movieid)
        rating = row['rating']
        timestamp = row['timestamp']
        date = datetime.fromtimestamp(timestamp)
        Review.objects.create(
            user=user,
            movie=movie,
            rating=int(float(rating)*2),
            created_at=date,
            updated_at=date
        )
        print(f"rating {index} added", end='\r')


@timed
def removing_ratings(apps, schema):
    Review = apps.get_model('app', 'Review')
    Review.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_add_review_model'),
    ]

    operations = [
        migrations.RunPython(
            add_ratings,
            reverse_code=removing_ratings,
        ),
    ]
