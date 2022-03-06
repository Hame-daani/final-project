from math import sqrt
from app.models import User, Movie


def get_ratings(p1, p2, data):
    similars = list(set([t for t, r in data[p1]]) & set([t for t, r in data[p2]]))
    p1_ratings = [r for t, r in data[p1] if t in similars]
    p2_ratings = [r for t, r in data[p2] if t in similars]
    return p1_ratings, p2_ratings


def sim_pearson(p1, p2, data):
    p1_ratings, p2_ratings = get_ratings(p1, p2, data)
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
        total = 0
        sim_sum = 0
        for friend in user.friends.all():
            try:
                review = friend.reviews.get(movie=movie)
                friend_sim = user.similarities.get(target=friend).score
                sim_sum += friend_sim
                total += friend_sim * review.rating
            except:
                continue
        return round(total / sim_sum, 1)
