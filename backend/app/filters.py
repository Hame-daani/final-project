from django_filters import filters, FilterSet

from .models import Movie


class MovieFilter(FilterSet):
    genres = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Movie
        fields = ("year", "genres")
