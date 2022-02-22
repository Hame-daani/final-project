from django.db import migrations, models
import pandas as pd


def add_movies(apps, schema):
    print("\n-----start adding movies-----")
    df_movies = pd.read_csv('data/movies.csv', low_memory=False)
    df_links = pd.read_csv('data/links.csv', low_memory=False)
    df = df_movies.set_index("movieId").join(df_links.set_index("movieId"))
    Movie = apps.get_model('app', 'Movie')
    for index, row in df.iterrows():
        id = index
        title = row['title']
        a = title.rfind('(')
        b = title.rfind(')')
        year = title[a+1:b]
        if not year.isdigit():
            year = ''
        title = title[:a]
        genres = row['genres'].split('|')
        imdbid = row['imdbId']
        tmdbid = row['tmdbId']
        Movie.objects.create(
            id=id,
            title=title,
            year=year,
            genres=genres,
            imdbid=imdbid,
            tmdbid=tmdbid,
        )
        print(f"movie {index} added", end='\r')
    print("\n-----finished adding movies-----")


def reverse_add_movies(apps, schema):
    print("\n-----start removing movies-----")
    Movie = apps.get_model('app', 'Movie')
    Movie.objects.all().delete()
    print("\n-----finished removing movies-----")


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
