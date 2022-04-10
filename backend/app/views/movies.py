from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from app.models import Movie
from app.serializers import MovieSerializer
from app.filters import MovieFilter


class MovieViewSet(ReadOnlyModelViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MovieFilter
    search_fields = ["^title"]
    ordering_fields = ["year"]
