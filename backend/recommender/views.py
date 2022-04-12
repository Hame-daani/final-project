from rest_framework.generics import ListAPIView

from recommender.module import GlobalRecommender
from app.serializers import MovieSerializer


class smView(ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return GlobalRecommender.get_similar_movies(pk)
