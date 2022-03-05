from datetime import datetime
from celery import shared_task
from config.celery import app
from celery.schedules import crontab

from django.contrib.contenttypes.models import ContentType

from recommender.module import sim_pearson
from recommender.models import Similarity
from app.models import User, Movie

tasks_time = crontab(minute=30)

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
    return


@shared_task
def generate_uu_data():
    print("deleting data")
    Similarity.objects.filter(
        content_type=ContentType.objects.get_for_model(User)
    ).delete()
    start = datetime.now()
    print("start uu_data")
    users = User.objects.order_by("id")[:100]
    for user1 in users:
        for user2 in users:
            if user1 == user2:
                continue
            else:
                try:
                    obj = Similarity.objects.get(
                        content_type=ContentType.objects.get_for_model(user1),
                        source_id=user1.id,
                        target_id=user2.id,
                    )
                    continue
                except:
                    Similarity.objects.create(
                        source=user1, target=user2, score=sim_pearson(user1, user2)
                    )
        print(f"user{user1.id} done!")
    finish = datetime.now()
    print(f"task uu_data finsihed in {finish-start}")
