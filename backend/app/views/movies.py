from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from app.models import Movie
from app.serializers import MovieSerializer
from app.filters import MovieFilter
from recommender.module import FriendsRecommender
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
                instance.er = r["rating"]
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
