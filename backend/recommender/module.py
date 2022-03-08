from math import sqrt
from app.models import Review, User, Movie
from django.db.models import F, Sum, Case, When, FloatField


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
        Ex.time: 800 ms
        """

        myfriends = user.friends.all()
        results = (
            Review.objects.filter(movie=movie)
            .filter(user__in=myfriends)
            .filter(user__similarities__target_id=user.id)
            .aggregate(
                sim_sum=Sum("user__similarities__score"),
                total=Sum(F("user__similarities__score") * F("rating")),
            )
        )
        sim_sum, total = results["sim_sum"], results["total"]
        # total = 0
        # sim_sum = 0
        # for friend in user.friends.all():
        #     try:
        #         r = friend.reviews.get(movie=movie)
        #         fs = user.similarities.get(target_id=friend.id).score
        #         sim_sum += fs
        #         total += fs * r.rating
        #     except:
        #         continue
        if not sim_sum or not total:
            return 0
        return {"rating": int(total // sim_sum), "sim": float(sim_sum)}

    @staticmethod
    def get_recommendation(user: User):
        """
        return top 10 movies calculated from friends
        Ex.time: 4.13 ms
        """
        myfriends = user.friends.all()
        movies = (
            Movie.objects.exclude(reviews__user=user)
            .filter(
                reviews__user__in=myfriends,
                reviews__user__similarities__target_id=user.id,
            )
            .annotate(sim_sum=Sum(F("reviews__user__similarities__score")))
            .annotate(
                total=Sum(
                    F("reviews__user__similarities__score") * F("reviews__rating")
                )
            )
            .annotate(
                er=Case(
                    When(sim_sum=0, then=0),
                    default=F("total") / F("sim_sum"),
                    output_field=FloatField(),
                )
            )
        )

        return movies.order_by("-er")[:10]


class GlobalRecommender:
    @staticmethod
    def get_TCS(me, user):
        try:
            return float(me.similarities.get(target_id=user.id).score)
        except:
            return 0

    @staticmethod
    def get_taste_group(user):
        return (
            User.objects.filter(similarities__target_id=user.id)
            .annotate(sim=F("similarities__score"))
            .order_by("-sim")[:100]
        )
