from app.models import *


class BaseRecommender:
    def __init__(self) -> None:
        pass

    @property
    def uu_data():
        """
        return df loaded from csv file
        """
        pass


class GlobalRecommender(BaseRecommender):

    def __init__(self) -> None:
        super().__init__()

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

    def get_estimated_rating(self, user, movie):
        """
        return estimated rating for a movie.
        formoula: [similariy*rating for all in myfriends] / sum(similarities)
        """
        return 5

    def get_recommendation(self, user):
        """
        return top 10 movies based on mm_data from my friends
        """
