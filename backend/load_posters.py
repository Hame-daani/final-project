import asyncio
import aiohttp
import pandas as pd
from asgiref import sync
import time
import bs4
from async_retrying import retry
from aiohttp_retry import RetryClient, ExponentialRetry


def timed(func):
    """
    records approximate durations of function calls
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f'\n{func.__name__} started')
        result = func(*args, **kwargs)
        print(f"\n{func.__name__} finished in {time.time() - start:.2f} seconds")
        return result
    return wrapper


i = 0
j = 0

statuses = {x for x in range(100, 600)}
statuses.remove(200)
statuses.remove(429)


@timed
def async_aiohttp_get_all(urls):
    """
    performs asynchronous get requests
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    async def get_all(urls):
        async with aiohttp.ClientSession() as session:
            @retry(attempts=5)
            async def fetch(url):
                global i, j
                i += 1
                print(f"get {i} finished {j}", end='\r')
                async with session.get(url, raise_for_status=True) as response:
                    print(f"get {i} finished {j}", end='\r')
                    j += 1
                    return await response.text()
            return await asyncio.gather(*[
                fetch(url) for url in urls
            ])
    return sync.async_to_sync(get_all)(urls)


@ timed
def get_posters(pages, selector):
    posters = []
    k = 0
    base = "http://www.themoviedb.org"
    for page in pages:
        k += 1
        try:
            soup = bs4.BeautifulSoup(page, 'html.parser')
            data = soup.select_one(selector)
            # posters.append(base+data['data-src'])
            posters.append(base+data['data-src'][4])
        except:
            print(soup.title.text)
            posters.append('')
        print(f"get {k} poster", end='\r')
    return posters


if __name__ == '__main__':
    df_movies = pd.read_csv('data/movies.csv', low_memory=False)
    df_links = pd.read_csv('data/links.csv', low_memory=False)
    df = df_movies.set_index("movieId").join(df_links.set_index("movieId"))
    n = 100
    results = df[:n] if n else df

    # ids = results['tmdbId']
    # base = "https://www.themoviedb.org/movie/"
    # urls = [f"{base}{id:.0f}" for id in ids]
    # selector = "img.poster"

    ids = results['imdbId']
    base = "https://www.imdb.com/title/tt"
    urls = [f"{base}{id:07}" for id in ids]
    selector = "img.ipc-image"

    pages = async_aiohttp_get_all(urls)
    posters = get_posters(pages, selector)
    results['poster'] = posters
    # print(results[['tmdbId', 'poster']].to_string(index=False))
    # print(*posters, sep='\n')
    results.to_csv('data/movies_full.csv')
