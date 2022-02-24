from django.db import migrations, models
import pandas as pd
from datetime import datetime
from app.utils import timed
from faker import Faker
from faker.providers import lorem


@timed
def add_ratings(apps, schema):
    df = pd.read_csv('data/ratings_clean.csv', low_memory=False)
    Review = apps.get_model('app', 'Review')
    Movie = apps.get_model('app', 'Movie')
    User = apps.get_model('app', 'User')
    faker = Faker()
    Faker.seed(0)
    faker.add_provider(lorem)
    for index, row in df.iterrows():
        userid = row['userId']
        movieid = row['movieId']
        user = User.objects.get(id=userid)
        movie = Movie.objects.get(id=movieid)
        rating = row['rating']
        timestamp = row['timestamp']
        date = datetime.fromtimestamp(timestamp)
        text = faker.sentence(nb_words=10)
        Review.objects.create(
            user=user,
            movie=movie,
            text=text,
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
        ('app', '0007_add_review_model'),
    ]

    operations = [
        migrations.RunPython(
            add_ratings,
            reverse_code=removing_ratings,
        ),
        migrations.operations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True)
        ),
        migrations.operations.AlterField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True)
        ),
    ]
