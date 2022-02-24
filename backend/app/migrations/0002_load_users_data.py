from django.db import migrations
from faker import Faker
from faker.providers import address, person
from app.utils import timed


@timed
def add_users(apps, schema):
    faker = Faker()
    Faker.seed(0)
    faker.add_provider(address)
    faker.add_provider(person)
    User = apps.get_model('app', 'User')
    for i in range(5000):
        first_name = faker.first_name()
        last_name = faker.last_name()
        username = first_name+last_name+str(i)
        email = f"{username}@this.com"
        gender = 'M' if i % 2 else 'F'
        location = faker.city()
        User.objects.create(
            id=i,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password='12345678',
            gender=gender,
            location=location
        )
        print(f"user {i} added", end='\r')


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
