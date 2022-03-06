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
    start = datetime.now()
    logging.warning("start mm_data")
    logging.warning(f"calculating for {n} movies")
    for i, movie1 in enumerate(movie_ids):
        # if similarities.count() == (n - 1):
        #     logging.warning(f"movie {movie1} already done!")
        #     continue
        for movie2 in movie_ids:
            if movie1 >= movie2:
                continue
            else:
                Similarity.objects.create(
                    content_type=ct,
                    source_id=movie1,
                    target_id=movie2,
                    score=sim_pearson(movie1, movie2, data),
                )
        logging.warning(f"movie {i+1} done!")
    finish = datetime.now()
    logging.error(f"task mm_data finsihed in {finish-start}")


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
    start = datetime.now()
    logging.warning("start uu_data")
    logging.warning(f"calculating for {n} users")
    for i, user1 in enumerate(user_ids):
        # if user1.similarities.count() == (n - 1):
        #     logging.warning(f"user {user1.id} already done!")
        #     continue
        for user2 in user_ids:
            if user1 >= user2:
                continue
            else:
                Similarity.objects.create(
                    content_type=ct,
                    source_id=user1,
                    target_id=user2,
                    score=sim_pearson(user1, user2, data),
                )
        logging.warning(f"user {i+1} done!")
    finish = datetime.now()
    logging.warning(f"task uu_data finsihed in {finish-start}")
