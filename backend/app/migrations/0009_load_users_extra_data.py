from django.db import migrations
from app.utils import timed
import pandas as pd
import ast
import threading


@timed
def add_friends(apps, schema):
    df = pd.read_csv("data/users.csv", low_memory=False)
    #     d = len(df) // 3
    #     t1 = threading.Thread(target=adder_child, args=(apps, schema, df[:d]))
    #     t2 = threading.Thread(target=adder_child, args=(apps, schema, df[d : d * 2]))
    #     t3 = threading.Thread(target=adder_child, args=(apps, schema, df[d * 2 :]))
    #     t1.start()
    #     t2.start()
    #     t3.start()
    #     t1.join()
    #     t2.join()
    #     t3.join()

    # def adder_child(apps, schema, df):
    User = apps.get_model("app", "User")
    for index, row in df.iterrows():
        user = User.objects.get(id=row["id"])
        friends = ast.literal_eval(row["friends"])
        user.friends.add(*friends)
        watchlist = ast.literal_eval(row["watchlist"])
        user.watchlist.add(*watchlist)
        favorites = ast.literal_eval(row["favorites"])
        user.favorites.add(*favorites)
        user.save()
        print(f"user {index} done", end="\r")


@timed
def removing_friends(apps, schema):
    User = apps.get_model("app", "User")
    for user in User.objects.all():
        user.friends.clear()
        user.favorites.clear()
        user.watchlist.clear()
        user.save()
        print(f"user {user.id} extra data removed", end="\r")


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
