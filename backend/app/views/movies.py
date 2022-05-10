from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from app.models import Movie
from app.serializers import MovieSerializer, UserSerializer
from app.filters import MovieFilter
from recommender.module import FriendsRecommender, GlobalRecommender
from app.mixins import Likeable


class MovieViewSet(ReadOnlyModelViewSet, Likeable):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = MovieFilter
    search_fields = ["^title"]
    ordering_fields = ["year"]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated:
            r = FriendsRecommender.get_estimated_rating(request.user, instance)
            if r:
                instance.friends_er = r["rating"]
            r = GlobalRecommender.get_estimated_rating(request.user, instance)
            if r:
                instance.global_er = r["rating"]
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["GET", "POST", "DELETE"])
    def watchlist(self, request, pk=None):
        if request.method == "POST":
            try:
                obj = self.get_object()
                obj.watchlist.add(request.user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if request.method == "GET":
            obj = self.get_object()
            q = obj.watchlist.all()
            return Response(
                UserSerializer(q, many=True).data,
                status=status.HTTP_200_OK,
            )
        if request.method == "DELETE":
            try:
                obj = self.get_object()
                obj.watchlist.remove(request.user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
