from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from recommender.module import GlobalRecommender
from app.serializers import MovieSerializer, UserSerializer


class smView(ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return GlobalRecommender.get_similar_movies(pk)


class suView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        u = self.request.user
        return GlobalRecommender.get_taste_group(u)
