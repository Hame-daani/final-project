from django.db import migrations, models
from faker import Faker
from faker.providers import address, person


def add_users(apps, schema):
    print("\n-----start adding users-----")
    faker = Faker()
    Faker.seed(0)
    faker.add_provider(address)
    faker.add_provider(person)
    User = apps.get_model('app', 'User')
    for i in range(162541):
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
    print("\n-----finished adding users-----")


def reverse_add_users(apps, schema):
    print("\n-----start removing users-----")
    User = apps.get_model('app', 'User')
    User.objects.all().delete()
    print("\n-----finished removing users-----")


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_add_user_model'),
    ]

    operations = [
        migrations.RunPython(
            add_users,
            reverse_code=reverse_add_users,
        ),
    ]
