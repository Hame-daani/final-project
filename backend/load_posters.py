import asyncio
import aiohttp
import pandas as pd
from asgiref import sync
import time
import bs4
from async_retrying import retry


def timed(func):
    """
    records approximate durations of function calls
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        print('{name:<30} started'.format(name=func.__name__))
        result = func(*args, **kwargs)
        duration = "{name:<30} finished in {elapsed:.2f} seconds".format(
            name=func.__name__, elapsed=time.time() - start
        )
        print(duration)
        timed.durations.append(duration)
        return result
    return wrapper


timed.durations = []

i = 0
j = 0


@timed
def async_aiohttp_get_all(urls):
    """
    performs asynchronous get requests
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    async def get_all(urls):
        async with aiohttp.ClientSession(headers=headers) as session:
            @retry(attempts=3)
            async def fetch(url):
                global i, j
                i += 1
                print(f"get {i} finished {j}", end='\r')
                async with session.get(url) as response:
                    print(f"get {i} finished {j}", end='\r')
                    j += 1
                    return await response.text()
            return await asyncio.gather(*[
                fetch(url) for url in urls
            ])
    return sync.async_to_sync(get_all)(urls)


if __name__ == '__main__':
    df_movies = pd.read_csv('data/movies.csv', low_memory=False)
    df_links = pd.read_csv('data/links.csv', low_memory=False)
    df = df_movies.set_index("movieId").join(df_links.set_index("movieId"))
    ids = df['tmdbId']
    base = "https://www.themoviedb.org/movie/"
    selector = "img.poster"
    urls = [f"{base}{id:.0f}" for id in ids]
    pages = async_aiohttp_get_all(urls)
    posters = []
    for page in pages:
        try:
            soup = bs4.BeautifulSoup(page, 'html.parser')
            data = soup.select_one(selector)
            posters.append(data['data-src'])
        except:
            posters.append('')
    results = df
    results['poster'] = posters
    results.to_csv('data/movies_full.csv')
