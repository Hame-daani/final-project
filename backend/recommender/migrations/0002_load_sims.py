from django.db import migrations
import pandas as pd
from app.utils import timed
from tqdm import tqdm

from app.models import User, Movie


@timed
def add_sims(apps, schema):
    Similarity = apps.get_model("recommender", "Similarity")
    ContentType = apps.get_model("contenttypes", "ContentType")
    cts = {
        6: ContentType.objects.get_for_model(User),
        7: ContentType.objects.get_for_model(Movie),
    }

    chunksize = 10**6
    with pd.read_csv(
        "data/postgresql/similarities.csv", chunksize=chunksize, iterator=True
    ) as reader:
        for df in reader:
            cache = []
            cache_size = 1000
            counter = 0
            for index, row in tqdm(df.iterrows(), total=df.shape[0]):
                id = row[0]
                source_id = row[1]
                target_id = row[2]
                score = row[3]
                ct = cts[int(row[4])]
                cache.append(
                    Similarity(
                        id=id,
                        content_type=ct,
                        source_id=source_id,
                        target_id=target_id,
                        score=score,
                    )
                )
                counter += 1
                if counter % cache_size == 0:
                    Similarity.objects.bulk_create(cache)
                    del cache
                    cache = []
            Similarity.objects.bulk_create(cache)


@timed
def removing_sims(apps, schema):
    Similarity = apps.get_model("recommender", "Similarity")
    Similarity.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("recommender", "0001_add_similarity_model"),
    ]

    operations = [
        # migrations.RunPython(
        #     add_sims,
        #     reverse_code=removing_sims,
        # ),
    ]
