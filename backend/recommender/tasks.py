from datetime import datetime
import logging
import threading
from enum import Enum

from celery import shared_task
from config.celery import app
from celery.schedules import crontab

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from recommender.module import sim_pearson
from recommender.models import Similarity
from app.models import User, Movie

# movies_time = crontab(hour="*", minute=4)
# users_time = crontab(hour="*", minute=4)

tasks_time = crontab(hour="*", minute=50)

app.conf.beat_schedule = {
    "Generate_User-User_Data": {
        "task": "recommender.tasks.generate_uu_data",
        "schedule": tasks_time,
    },
    #     "Generate_Movie-Movie_data": {
    #         "task": "recommender.tasks.generate_mm_data",
    #         "schedule": tasks_time,
    #     },
}

target_num = 100


class Ttype(Enum):
    odd_odd = 1
    even_even = 2
    odd_even = 3


def isodd(n):
    return n % 2 != 0


def iseven(n):
    return n % 2 == 0


@shared_task
def generate_mm_data():
    Similarity.truncate()
    ct = ContentType.objects.get_for_model(Movie)
    movies = Movie.objects.annotate(rcount=Count("reviews__id"))
    # 702 movies
    movies = movies.filter(rcount__gt=10)[:target_num]
    data = {
        movie.id: list(movie.reviews.values_list("user", "rating")) for movie in movies
    }
    movie_ids = list(movies.values_list("id", flat=True))
    n = len(movie_ids)
    logging.warning(
        f"start mm_data with {Similarity.objects.filter(content_type=ct).count()}"
    )
    start = datetime.now()
    logging.warning(f"calculating for {n} movies")
    t1 = threading.Thread(target=calculating, args=(ct, movie_ids, data, Ttype.odd_odd))
    t2 = threading.Thread(
        target=calculating, args=(ct, movie_ids, data, Ttype.odd_even)
    )
    t3 = threading.Thread(
        target=calculating, args=(ct, movie_ids, data, Ttype.even_even)
    )
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    finish = datetime.now()
    logging.error(
        f"task mm_data finsihed in {finish-start} with {Similarity.objects.filter(content_type=ct).count()}"
    )


@shared_task
def generate_uu_data():
    Similarity.truncate()
    ct = ContentType.objects.get_for_model(User)
    users = User.objects.annotate(rcount=Count("reviews__id"))
    # 3303 users
    users = users.filter(rcount__gt=10)[:target_num]
    data = {
        user.id: list(user.reviews.values_list("movie", "rating")) for user in users
    }
    user_ids = list(users.values_list("id", flat=True))
    n = len(user_ids)
    logging.warning(
        f"start uu_data {Similarity.objects.filter(content_type=ct).count()}"
    )
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
    logging.error(
        f"finished uu_data in {finish-start} with {Similarity.objects.filter(content_type=ct).count()}"
    )


def calculating(ct, ids, data, ttype=1):
    counter = 0
    for i, t1 in enumerate(ids):
        if i % 100 == 0:
            logging.info(f"worker:{ct.model}:{ttype.value} - reached {i}")
        if iseven(i) and ttype == Ttype.odd_odd:
            continue
        if isodd(i) and ttype == Ttype.even_even:
            continue
        for j, t2 in enumerate(reversed(ids)):
            if t1 == t2:
                break
            if iseven(j) and ttype == Ttype.odd_odd:
                continue
            if isodd(j) and ttype == Ttype.even_even:
                continue
            if ttype == Ttype.odd_even:
                if isodd(i) and isodd(j):
                    continue
                if iseven(i) and iseven(j):
                    continue
            counter += 1
            Similarity.objects.create(
                content_type=ct,
                source_id=t1,
                target_id=t2,
                score=sim_pearson(data[t1], data[t2]),
            )
    logging.warning(f"worker:{ct.model}:{ttype.value} - finished {counter} created")
