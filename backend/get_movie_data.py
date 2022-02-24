import requests
import bs4
import pandas as pd
from app.utils import timed

selector_poster = "img.poster"
selector_plot = "div.overview"
base = "https://www.themoviedb.org"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


@timed
def get_data(ids):
    posters = []
    plots = []
    for i, id in enumerate(ids):
        url = f"{base}/movie/{id:07}"
        page = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        try:
            data = soup.select_one(selector_poster)
            posters.append(base+data['data-src'])
        except:
            posters.append('')
            print(f"\ncouldnt get poster for {id}")
        try:
            data = soup.select_one(selector_plot)
            plots.append(data.p.text)
        except:
            plots.append('')
            print(f"\ncouldnt get plot for {id}")
        print(f"movie {i} done", end='\r')
    return posters, plots


if __name__ == '__main__':
    df = pd.read_csv('data/movies_clean.csv', low_memory=False)
    ids = df['tmdbId']
    posters, plots = get_data(ids)
    df['poster'] = posters
    df['plot'] = plots
    df.to_csv('data/movies_clean.csv', index=False)
