import pandas as pd
from app.utils import timed
from faker import Faker
from faker.providers import address, person, lorem
from random import randint


@timed
def get_data():
    users = []
    min_id = 1
    max_id = 5000
    min_id_movie = 1
    max_id_movie = 999
    missing_movie_ids = [
        91,
        221,
        291,
        323,
        545,
        557,
        578,
        622,
        624,
        646,
        669,
        677,
        686,
        689,
        740,
        811,
        817,
        863,
        883,
        888,
        978,
        995,
    ]
    faker = Faker()
    Faker.seed(0)
    faker.add_provider(address)
    faker.add_provider(person)
    faker.add_provider(lorem)
    for i in range(min_id, max_id + 1):
        first_name = faker.first_name()
        last_name = faker.last_name()
        username = first_name+last_name+str(i)
        email = f"{username}@this.com"
        gender = 'M' if i % 2 else 'F'
        location = faker.city()
        bio = faker.sentence(nb_words=10)
        # friends
        n = randint(1, 100)
        friends = []
        for _ in range(n):
            pk = randint(min_id, max_id)
            if pk != i:
                friends.append(pk)
        # watchlist
        n = randint(1, 100)
        watchlist = []
        for _ in range(n):
            pk = randint(min_id_movie, max_id_movie)
            if pk != i and pk not in missing_movie_ids:
                watchlist.append(pk)
        # favorites
        n = randint(1, 100)
        favorites = []
        for _ in range(n):
            pk = randint(min_id_movie, max_id_movie)
            if pk != i and pk not in missing_movie_ids:
                favorites.append(pk)
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
                'friends': friends,
                'favorites': favorites,
                'watchlist': watchlist
            }
        )
        print(f"user {i} added", end='\r')
    return users


if __name__ == '__main__':
    users = get_data()
    df = pd.DataFrame(users)
    df.to_csv('data/users.csv', index=False)
