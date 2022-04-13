from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from recommender.module import GlobalRecommender, FriendsRecommender
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


class GlobalRecommendationView(ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        u = self.request.user
        return GlobalRecommender.get_recommendation(u)


class FriendsRecommendationView(ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        u = self.request.user
        return FriendsRecommender.get_recommendation(u)
