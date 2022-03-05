import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("myapp")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(hour=13, minute=13),
#         generating_mm_data.s()
#     )
#     sender.add_periodic_task(
#         crontab(hour=13, minute=13),
#         generating_uu_data.s()
#     )

app.conf.beat_schedule = {
    "add-every-5-seconds": {"task": "app.tasks.generating_uu_data", "schedule": 5.0}
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
