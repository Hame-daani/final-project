from datetime import datetime
import logging
import threading
from enum import Enum

from celery import shared_task
from config.celery import app
from celery.schedules import crontab

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.db import connection

from recommender.module import sim_pearson
from recommender.models import Similarity
from app.models import User, Movie

tasks_time = crontab(hour=20, minute=58)

app.conf.beat_schedule = {
    "Generate_User-User_Data": {
        "task": "recommender.tasks.generate_uu_data",
        "schedule": tasks_time,
    },
    # "Generate_Movie-Movie_data": {
    #     "task": "recommender.tasks.generate_mm_data",
    #     "schedule": tasks_time,
    # },
}


class Ttype(Enum):
    odd_odd = 1
    even_even = 2
    odd_even = 3


@shared_task
def generate_mm_data():
    Similarity.truncate()
    ct = ContentType.objects.get_for_model(Movie)
    movies = Movie.objects.annotate(rcount=Count("reviews__id"))
    # 450 movies
    movies = movies.filter(rcount__gt=50)[:100]
    data = {
        movie.id: list(movie.reviews.values_list("user", "rating")) for movie in movies
    }
    movie_ids = list(movies.values_list("id", flat=True))
    n = len(movie_ids)
    logging.warning(f"start mm_data with {Similarity.objects.count()}")
    start = datetime.now()
    logging.warning(f"calculating for {n} movies")
    t1 = threading.Thread(target=calculating, args=(ct, movie_ids, data, 1))
    t2 = threading.Thread(target=calculating, args=(ct, movie_ids, data, 2))
    t3 = threading.Thread(target=calculating, args=(ct, movie_ids, data, 3))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    finish = datetime.now()
    logging.error(
        f"task mm_data finsihed in {finish-start} with {Similarity.objects.count()}"
    )


@shared_task
def generate_uu_data():
    Similarity.truncate()
    ct = ContentType.objects.get_for_model(User)
    users = User.objects.annotate(rcount=Count("reviews__id"))
    # 320 users
    users = users.filter(rcount__gt=10)[:100]
    data = {
        user.id: list(user.reviews.values_list("movie", "rating")) for user in users
    }
    user_ids = list(users.values_list("id", flat=True))
    n = len(user_ids)
    logging.warning(f"start uu_data {Similarity.objects.count()}")
    start = datetime.now()
    logging.warning(f"calculating for {n} users")
    t1 = threading.Thread(target=calculating, args=(ct, user_ids, data, Ttype.odd_odd))
    t2 = threading.Thread(target=calculating, args=(ct, user_ids, data, Ttype.odd_even))
    t3 = threading.Thread(
        target=calculating, args=(ct, user_ids, data, Ttype.even_even)
    )
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    finish = datetime.now()
    logging.warning(
        f"finished uu_data in {finish-start} with {Similarity.objects.count()}"
    )


def calculating(ct, ids, data, ttype=1):
    connection.connect()
    for i, t1 in enumerate(ids):
        # if user1.similarities.count() == (n - 1):
        #     logging.warning(f"user {user1.id} already done!")
        #     continue
        if ttype == Ttype.odd_odd:
            if i % 2 == 0:
                continue
        if ttype == Ttype.even_even:
            if i % 2 != 0:
                continue
        for j, t2 in enumerate(reversed(ids)):
            if i == j:
                break
            if ttype == Ttype.odd_odd and j % 2 == 0:
                continue
            if ttype == Ttype.even_even and j % 2 != 0:
                continue
            if ttype == Ttype.odd_even:
                if i % 2 != 0 and j % 2 != 0:
                    continue
                if i % 2 == 0 and j % 2 == 0:
                    continue
            Similarity.objects.create(
                content_type=ct,
                source_id=t1,
                target_id=t2,
                score=sim_pearson(t1, t2, data),
            )
        print(f"worker:{ttype.name} {ct.model}-{i} done!")
