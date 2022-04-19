from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from app.models import Movie, Review
from app.serializers import ReviewSerializer
from app.permissions import isOwner
from app.mixins import Commentable, Likeable


class ReviewViewSet(ModelViewSet, Commentable, Likeable):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (isOwner,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["user", "movie"]
    ordering_fields = ["created_at"]

    def create(self, request, *args, **kwargs):
        movie_id = request.data["movie"]
        movie = Movie.objects.get(id=movie_id)
        obj = Review(user=request.user, movie=movie)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def recent(self, request):
        queryset = Review.objects.order_by("-created_at")[:10]
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def friends(self, request):
        user = request.user
        if user.is_authenticated:
            friends = user.friends.all()
            queryset = Review.objects.filter(user__in=friends).order_by("-created_at")[
                :10
            ]
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                data={"you need to sign in"}, status=status.HTTP_401_UNAUTHORIZED
            )
