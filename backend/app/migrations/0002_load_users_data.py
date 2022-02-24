from django.db import migrations
import pandas as pd
from app.utils import timed


@timed
def add_users(apps, schema):
    df = pd.read_csv('data/users.csv', low_memory=False)
    User = apps.get_model('app', 'User')
    for index, row in df.iterrows():
        User.objects.create(
            id=row['id'],
            username=row['username'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            password='12345678',
            bio=row['bio'],
            gender=row['gender'],
            location=row['location']
        )
        print(f"user {index} added", end='\r')


def removing_users(apps, schema):
    User = apps.get_model('app', 'User')
    User.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_add_user_model'),
    ]

    operations = [
        migrations.RunPython(
            add_users,
            reverse_code=removing_users,
        ),
    ]
