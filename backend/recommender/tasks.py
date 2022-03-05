import logging
from celery.utils.log import get_task_logger
from celery import shared_task
from app.models import Movie
from datetime import datetime
from config.celery import app
from celery.schedules import crontab


logger = logging.getLogger(__name__)

tasks_time = crontab(minute=16)

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
    now = datetime.now()
    print(f"start mm_data at {now.hour}:{now.minute}")
    for _ in range(100000000):
        pass
    logger.warn("task finsihed")


@shared_task
def generate_uu_data():
    now = datetime.now()
    print(f"start uu_data at {now.hour}:{now.minute}")
    for _ in range(100000000):
        pass
    print("task finsihed")
