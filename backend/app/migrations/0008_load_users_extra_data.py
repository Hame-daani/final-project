from django.db import migrations
from app.utils import timed
import pandas as pd
import ast


@timed
def add_friends(apps, schema):
    User = apps.get_model('app', 'User')
    df = pd.read_csv('data/users.csv', low_memory=False)
    for index, row in df.iterrows():
        user = User.objects.get(id=row['id'])
        friends = ast.literal_eval(row['friends'])
        user.friends.add(*friends)
        watchlist = ast.literal_eval(row['watchlist'])
        user.watchlist.add(*watchlist)
        favorites = ast.literal_eval(row['favorites'])
        user.favorites.add(*favorites)
        user.save()
        # print(f"user {index} done", end='\r')


@timed
def removing_friends(apps, schema):
    User = apps.get_model('app', 'User')
    for user in User.objects.all():
        user.friends.clear()
        user.favorites.clear()
        user.watchlist.clear()
        user.save()
        # print(f"user {user.id} extra data removed", end='\r')


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_add_friendrequest_model'),
    ]

    operations = [
        migrations.RunPython(
            add_friends,
            reverse_code=removing_friends,
        ),
    ]
