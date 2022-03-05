from math import sqrt
from app.models import User, Movie
from numpy import sum as npsum


def get_ratings(p1, p2):
    type_p1 = type(p1)
    type_p2 = type(p2)
    if type_p1 != type_p2:
        raise Exception("got two diffrent thing!")
    if type_p1 == Movie:
        p2_reviews = p2.reviews.filter(
            user__id__in=p1.reviews.values_list("user", flat=True)
        )
        p1_reviews = p1.reviews.filter(
            user__id__in=p2_reviews.values_list("user", flat=True)
        )
        p1_ratings = p1_reviews.order_by("user").values_list("rating", flat=True)
        p2_ratings = p2_reviews.order_by("user").values_list("rating", flat=True)
    if type_p1 == User:
        p2_reviews = p2.reviews.filter(
            movie__id__in=p1.reviews.values_list("movie", flat=True)
        )
        p1_reviews = p1.reviews.filter(
            movie__id__in=p2_reviews.values_list("movie", flat=True)
        )
        p1_ratings = p1_reviews.order_by("movie").values_list("rating", flat=True)
        p2_ratings = p2_reviews.order_by("movie").values_list("rating", flat=True)
    return p1_ratings, p2_ratings


def sim_pearson(p1, p2):
    p1_ratings, p2_ratings = get_ratings(p1, p2)
    n = len(p1_ratings)
    if n == 0:
        return 0
    sum1 = sum(p1_ratings)
    sum2 = sum(p2_ratings)
    sum1sq = sum([pow(rating, 2) for rating in p1_ratings])
    sum2sq = sum([pow(rating, 2) for rating in p2_ratings])
    psum = sum([p1_ratings[i] * p2_ratings[i] for i in range(n)])
    num = psum - (sum1 * sum2 / n)
    den = sqrt((sum1sq - pow(sum1, 2) / n) * (sum2sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    return num / den
