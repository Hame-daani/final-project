import pandas as pd
from app.utils import timed
from faker import Faker
from faker.providers import address, person, lorem
from random import randint


@timed
def get_data():
    users = []
    min_id = 0
    max_id = 4999
    faker = Faker()
    Faker.seed(0)
    faker.add_provider(address)
    faker.add_provider(person)
    faker.add_provider(lorem)
    for i in range(5000):
        first_name = faker.first_name()
        last_name = faker.last_name()
        username = first_name+last_name+str(i)
        email = f"{username}@this.com"
        gender = 'M' if i % 2 else 'F'
        location = faker.city()
        bio = faker.sentence(nb_words=10)
        n = randint(0, 100)
        friends = []
        for _ in range(n):
            pk = randint(min_id, max_id)
            if pk != i:
                friends.append(pk)
        users.append(
            {
                'id': i,
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'gender': gender,
                'location': location,
                'bio': bio,
                'friends': friends
            }
        )
        print(f"user {i} added", end='\r')
    return users


if __name__ == '__main__':
    users = get_data()
    df = pd.DataFrame(users)
    df.to_csv('data/users.csv', index=False)
