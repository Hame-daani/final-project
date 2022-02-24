from django.db import migrations
import pandas as pd
from app.utils import timed


@timed
def add_movies(apps, schema):
    df = pd.read_csv('data/movies_clean.csv', low_memory=False)
    Movie = apps.get_model('app', 'Movie')
    for index, row in df.iterrows():
        id = row['movieId']
        title = row['title']
        a = title.rfind('(')
        b = title.rfind(')')
        year = title[a+1:b]
        if not year.isdigit():
            year = ''
        title = title[:a]
        genres = row['genres'].split('|')
        imdbid = row['imdbId']
        tmdbid = f"{row['tmdbId']:.0f}"
        poster = row['poster']
        plot = row['plot']
        Movie.objects.create(
            id=id,
            title=title,
            year=year,
            genres=genres,
            imdbid=imdbid,
            tmdbid=tmdbid,
            poster=poster,
            plot=plot
        )
        print(f"movie {index} added", end='\r')


@timed
def removing_movies(apps, schema):
    Movie = apps.get_model('app', 'Movie')
    Movie.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_generate_friends'),
    ]

    operations = [
        migrations.RunPython(
            add_movies,
            reverse_code=removing_movies,
        ),
    ]
