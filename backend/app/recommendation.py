from app.models import Movie, User


class BaseRecommender:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(BaseRecommender, cls).__new__(cls)
            # Put any initialization here.
            cls._instance.load_uu_data()
        return cls._instance

    def load_uu_data(self):
        """
        return df loaded from csv file
        """
        self.uu_data = "uu"


class GlobalRecommender(BaseRecommender):

    def __init__(self) -> None:
        self.load_mm_data()
        super().__init__()

    def load_mm_data(self):
        self.mm_data = "mm"

    def get_similar_movies(self, movie):
        """
        returns top 10 most similar movies based on mm_data
        """
        sims = self.mm_data[movie.id]
        sims_ids = sims.sort(reverse=True)[:10]
        return Movie.objects.filter(id__in=sims_ids)

    def get_TCS(self, me, user):
        """
        returns user TCS based on my row in uu_data
        0 < TCS < 1
        """
        return self.uu_data[me.id][user.id]

    def get_taste_group(self, user):
        """
        return top 10 on my row in uu_data
        """

        group_ids = self.uu_data[user.id].sort(reverse=True)[:10]
        return User.objects.filter(id__in=group_ids)

    def get_recommendation(self, user):
        """
        return top 10 similar movies for my top 10 rated movies
        """
        my_top_10 = user.reviews.order_by('-rating')[:10]
        topmovies = []
        for movieid in my_top_10:
            topmovies.append(self.mm_data[movieid].sort(reverse=True)[:10])

        return Movie.objects.filter(id__in=topmovies)


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
            movie.estimated_rating = self.get_estimated_rating(movie)

        return ranking.order_by('-estimated_rating')[:10]


gr = GlobalRecommender()
fr = FriendsRecommender()
