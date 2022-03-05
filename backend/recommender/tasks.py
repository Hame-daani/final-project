from datetime import datetime
import logging

from celery import shared_task
from config.celery import app
from celery.schedules import crontab

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from recommender.module import sim_pearson
from recommender.models import Similarity
from app.models import User, Movie

tasks_time = crontab(hour=23, minute=6)

app.conf.beat_schedule = {
    "Generate_User-User_Data": {
        "task": "recommender.tasks.generate_uu_data",
        "schedule": tasks_time,
    },
    "Generate_Movie-Movie_data": {
        "task": "recommender.tasks.generate_mm_data",
        "schedule": tasks_time,
    },
}


@shared_task
def generate_mm_data():
    ct = ContentType.objects.get_for_model(Movie)
    start = datetime.now()
    logging.error("start mm_data")
    movies = Movie.objects.annotate(rcount=Count("reviews__id"))
    # 331 movies
    movies = movies.filter(rcount__gt=100)
    n = len(movies)
    logging.error(f"calculating for {n} movies")
    for i, movie1 in enumerate(movies):
        if movie1.similarities.count() == (n - 1):
            logging.error(f"movie {movie1.id} already done!")
            continue
        for movie2 in movies:
            if movie1 == movie2:
                continue
            else:
                try:
                    obj = Similarity.objects.get(
                        content_type=ct,
                        source_id=movie1.id,
                        target_id=movie2.id,
                    )
                    continue
                except:
                    Similarity.objects.create(
                        source=movie1, target=movie2, score=sim_pearson(movie1, movie2)
                    )
        logging.error(f"movie {i} done!")
    finish = datetime.now()
    logging.error(f"task mm_data finsihed in {finish-start}")


@shared_task
def generate_uu_data():
    ct = ContentType.objects.get_for_model(User)
    start = datetime.now()
    logging.warning("start uu_data")
    users = User.objects.annotate(rcount=Count("reviews__id"))
    # 320 users
    users = users.filter(rcount__gt=100)
    n = len(users)
    logging.warning(f"calculating for {n} users")
    for i, user1 in enumerate(users):
        if user1.similarities.count() == (n - 1):
            logging.warning(f"user {user1.id} already done!")
            continue
        for user2 in users:
            if user1 == user2:
                continue
            else:
                try:
                    obj = Similarity.objects.get(
                        content_type=ct,
                        source_id=user1.id,
                        target_id=user2.id,
                    )
                    continue
                except:
                    Similarity.objects.create(
                        source=user1, target=user2, score=sim_pearson(user1, user2)
                    )
        logging.warning(f"user {i} done!")
    finish = datetime.now()
    logging.warning(f"task uu_data finsihed in {finish-start}")
