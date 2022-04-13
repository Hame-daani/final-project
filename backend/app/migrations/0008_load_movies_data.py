from django.db import migrations
import pandas as pd
from app.utils import timed
from math import isnan
from tqdm import tqdm


@timed
def add_movies(apps, schema):
    df = pd.read_csv("data/postgresql/movies.csv", low_memory=False, delimiter="|")
    Movie = apps.get_model("app", "Movie")
    movies = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        id = row["id"]
        title = row["title"]
        year = row["year"]
        genres = row["genres"][1:-1].split(",")
        imdbid = row["imdbid"]
        if isnan(row["tmdbid"]):
            tmdbid = ""
        else:
            tmdbid = f"{row['tmdbid']:.0f}"
        poster = row["poster"]
        if type(poster) != str:
            poster = ""
        plot = row["plot"]
        if type(plot) != str:
            plot = ""
        movies.append(
            Movie(
                id=id,
                title=title,
                year=year,
                genres=genres,
                imdbid=imdbid,
                tmdbid=tmdbid,
                poster=poster,
                plot=plot,
            )
        )
    Movie.objects.bulk_create(movies)


@timed
def removing_movies(apps, schema):
    Movie = apps.get_model("app", "Movie")
    Movie.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_load_users_data"),
    ]

    operations = [
        migrations.RunPython(
            add_movies,
            reverse_code=removing_movies,
        ),
    ]
