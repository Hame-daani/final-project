import requests
from requests.exceptions import RequestException
import bs4
import logging
from datetime import datetime

from celery import shared_task
from config.celery import app
from celery.schedules import crontab
from celery import group
from celery.result import allow_join_result

from app.models import Movie

tasks_time = crontab(hour="*", minute=57)

app.conf.beat_schedule.update(
    {
        "Get Movies Poster Data": {
            "task": "app.tasks.get_movie_data",
            "schedule": tasks_time,
        },
    }
)

selector_poster = ".ipc-media__img"
base = "https://www.imdb.com/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}


@shared_task
def get_movie_data():
    success = 0
    failed = 0
    logging.warning(f"start get_movie_data")
    movies = Movie.objects.filter(poster="")
    start = datetime.now()
    jobs = []
    for mid in movies.values_list("imdbid", flat=True):
        jobs.append(get_poster_data.s(mid))
    g = group(jobs)
    res = g.delay()
    with allow_join_result():
        posters = res.get()
    logging.warning(f"got the posters")
    for i, movie in enumerate(movies):
        movie.poster = posters[i]
    logging.warning(f"updating database")
    Movie.objects.bulk_update(movies, ["poster"])
    finish = datetime.now()
    failed = posters.count("")
    success = len(posters) - failed
    logging.warning(
        f"task get_movie_data finsihed in {finish-start}. succes:{success} failed:{failed}"
    )


@shared_task(autoretry_for=(RequestException,), retry_backoff=True)
def get_poster_data(mid):
    url = f"{base}/title/tt{int(mid):07}"
    page = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    try:
        data = soup.select_one(selector_poster)
        return data.img["src"]

    except:
        logging.error(f"couldnt get poster for {mid}")
        return ""
