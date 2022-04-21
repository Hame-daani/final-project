from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.decorators import action

from app.models import User
from app.permissions import isSelf
from app.serializers import MovieSerializer, UserSerializer
from recommender.module import GlobalRecommender


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    permission_classes = (isSelf,)
    serializer_class = UserSerializer
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ["^username", "^first_name", "last_name"]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated:
            instance.sim = GlobalRecommender.get_TCS(request.user, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def friends(self, request, pk=None):
        try:
            obj = self.get_object()
            return Response(UserSerializer(obj.friends.all(), many=True).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def watchlist(self, request, pk=None):
        try:
            obj = self.get_object()
            queryset = obj.watchlist.all()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = MovieSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(
                MovieSerializer(obj.watchlist.all(), many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def favorites(self, request, pk=None):
        try:
            obj = self.get_object()
            return Response(MovieSerializer(obj.favorites.all(), many=True).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
