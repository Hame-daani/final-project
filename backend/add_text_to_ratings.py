import pandas as pd
from app.utils import timed
from faker import Faker
from faker.providers import lorem


@timed
def get_data():
    texts = []
    faker = Faker()
    Faker.seed(0)
    faker.add_provider(lorem)
    for i in range(n):
        texts.append(faker.sentence(nb_words=10))
        print(f"text {i} added", end='\r')
    return texts


if __name__ == '__main__':
    df = pd.read_csv('data/ratings.csv', low_memory=False)
    n = len(df)
    texts = get_data()
    df['text'] = texts
    df.to_csv('data/ratings.csv', index=False)
