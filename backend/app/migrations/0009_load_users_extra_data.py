from django.db import migrations
from app.utils import timed
import pandas as pd
import ast
from tqdm import tqdm


@timed
def add_friends(apps, schema):
    df = pd.read_csv("data/users.csv", low_memory=False)
    User = apps.get_model("app", "User")
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        user = User.objects.get(id=row["id"])
        friends = ast.literal_eval(row["friends"])
        user.friends.add(*friends)
        watchlist = ast.literal_eval(row["watchlist"])
        user.watchlist.add(*watchlist)
        favorites = ast.literal_eval(row["favorites"])
        user.favorites.add(*favorites)
        user.save()


@timed
def removing_friends(apps, schema):
    User = apps.get_model("app", "User")
    for user in tqdm(User.objects.all()):
        user.friends.clear()
        user.favorites.clear()
        user.watchlist.clear()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_load_movies_data"),
    ]

    operations = [
        migrations.RunPython(
            add_friends,
            reverse_code=removing_friends,
        ),
    ]
