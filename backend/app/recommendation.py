from app.models import Movie, User


class BaseRecommender:
    def __init__(self) -> None:
        self.load_uu_data()

    def load_uu_data(self):
        """
        return df loaded from csv file
        """
        pass


class GlobalRecommender(BaseRecommender):

    def __init__(self) -> None:
        self.load_mm_data()
        super().__init__()

    def load_mm_data(self):
        pass

    def get_similar_movies(self, movie):
        """
        returns top 10 most similar movies based on mm_data
        """
        return Movie.objects.all()[:10]

    def get_TCS(self, me, user):
        """
        returns user TCS based on my row in uu_data
        0 < TCS < 1
        """
        return 0.5

    def get_taste_group(self, user):
        """
        return top 10 on my row in uu_data
        """
        return user.friends.all()[:10]

    def get_recommendation(self, user):
        """
        return top 10 similar movies for my top 10 rated movies
        """
        return user.reviews.all()[:10]


class FriendsRecommender(BaseRecommender):

    def __init__(self) -> None:
        super().__init__()

    def get_estimated_rating(self, user: User, movie: Movie):
        """
        return estimated rating for a movie.
        formoula: [similariy*rating for all in myfriends] / sum(similarities)
        """
        sims = self.uu_data[user.id]
        total = 0
        sim_sum = 0
        for friend in user.friends.all():
            try:
                review = friend.reviews.get(movie=movie)
                friend_sim = sims[friend.id]
                sim_sum += friend_sim
                total += friend_sim*review.rating
            except:
                continue
        return round(total/sim_sum, 1)

    def get_recommendation(self, user: User):
        """
        return top 10 movies based on mm_data from my friends
        """
        my_movies = user.reviews.all().values_list('movie', flat=True)
        movies = Movie.objects.exclude(id__in=my_movies)
        ranking = []
        for movie in movies:
            ranking.append(self.get_estimated_rating(movie), movie)

        return ranking.sort(reverse=True)[:10]
