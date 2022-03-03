from celery.utils.log import get_task_logger
from celery import shared_task
from app.models import Movie
from datetime import datetime

logger = get_task_logger(__name__)


@shared_task
def generate_mm_data():
    now = datetime.now()
    print(f"start mm_data at {now.hour}:{now.minute}")
    print(Movie.objects.first().title)
    print("task finsihed")


@shared_task
def generate_uu_data():
    now = datetime.now()
    print(f"start uu_data at {now.hour}:{now.minute}")
    print(Movie.objects.last().title)
    print("task finsihed")
