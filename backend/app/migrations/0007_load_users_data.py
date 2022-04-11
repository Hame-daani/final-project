from django.db import migrations
import pandas as pd
from app.utils import timed

from django.contrib.auth.hashers import make_password


@timed
def add_users(apps, schema):
    df = pd.read_csv("data/postgresql/users.csv", low_memory=False, delimiter="|")
    User = apps.get_model("app", "User")
    users = []
    pw = make_password("12345678")
    for index, row in df.iterrows():
        users.append(
            User(
                username=row["username"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                password=pw,
                bio=row["bio"],
                gender=row["gender"],
                location=row["location"],
            )
        )
    User.objects.bulk_create(users)


@timed
def removing_users(apps, schema):
    User = apps.get_model("app", "User")
    User.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_add_like_model"),
    ]

    operations = [
        migrations.RunPython(
            add_users,
            reverse_code=removing_users,
        ),
    ]
