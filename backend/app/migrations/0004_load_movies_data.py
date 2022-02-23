from django.db import migrations, models
import pandas as pd
import time


def timed(func):
    """
    records approximate durations of function calls
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f'\n-----{func.__name__} started-----')
        func(*args, **kwargs)
        print(
            f"\n-----{func.__name__} finished in {time.time() - start:.2f} seconds-----")
    return wrapper


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
        poster = ''
        Movie.objects.create(
            id=id,
            title=title,
            year=year,
            genres=genres,
            imdbid=imdbid,
            tmdbid=tmdbid,
            poster=poster
        )
        print(f"movie {index} added", end='\r')


@timed
def reverse_add_movies(apps, schema):
    Movie = apps.get_model('app', 'Movie')
    Movie.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_add_movie_model'),
    ]

    operations = [
        migrations.RunPython(
            add_movies,
            reverse_code=reverse_add_movies,
        ),
    ]
