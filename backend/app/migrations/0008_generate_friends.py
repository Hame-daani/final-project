from random import randint
from django.db import migrations
from app.utils import timed


@timed
def add_friends(apps, schema):
    User = apps.get_model('app', 'User')
    min_id = 0
    max_id = 4999
    for user in User.objects.all():
        n = randint(0, 100)
        for _ in range(n):
            pk = randint(min_id, max_id)
            if pk != user.id:
                user.friends.add(User.objects.get(id=pk))
        print(f"user {user.id} got {n} friends", end='\r')


@timed
def removing_friends(apps, schema):
    User = apps.get_model('app', 'User')
    for user in User.objects.all():
        user.friends = None
        user.save()


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
