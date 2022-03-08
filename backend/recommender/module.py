from math import sqrt
from app.models import User, Movie
from django.db.models import F, Sum


def sim_pearson(data1, data2):
    similars = list(set([t for t, r in data1]) & set([t for t, r in data2]))
    p1_ratings = [r for t, r in data1 if t in similars]
    p2_ratings = [r for t, r in data2 if t in similars]
    n = len(p1_ratings)
    if n == 0:
        return 0
    sum1 = sum(p1_ratings)
    sum2 = sum(p2_ratings)
    sum1sq = sum([rating**2 for rating in p1_ratings])
    sum2sq = sum([rating**2 for rating in p2_ratings])
    psum = sum([p1_ratings[i] * p2_ratings[i] for i in range(n)])
    num = psum - (sum1 * sum2 / n)
    den = sqrt((sum1sq - pow(sum1, 2) / n) * (sum2sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    return num / den


class FriendsRecommender:
    @staticmethod
    def get_estimated_rating(user: User, movie: Movie):
        """
        return estimated rating for a movie.
        formoula: [similariy*rating for all in myfriends] / sum(similarities)
        """
        friends = user.friends.filter(
            reviews__movie=movie, similarities__target_id=user.id
        ).annotate(rating=F("reviews__rating"), sim=F("similarities__score"))
        sim_sum = friends.aggregate(sum=Sum("sim"))["sum"]
        total = friends.aggregate(total=Sum(F("sim") * F("rating")))["total"]
        return {"rating": int(total // sim_sum), "sim": float(sim_sum)}
