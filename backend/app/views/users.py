from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.decorators import action

from app.models import Movie, User
from app.permissions import isSelf
from app.serializers import LikeSerializer, MovieSerializer, UserSerializer
from recommender.module import GlobalRecommender

from django.contrib.contenttypes.models import ContentType


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
    def following(self, request, pk=None):
        try:
            obj = self.get_object()
            queryset = obj.following.all()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = UserSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(
                UserSerializer(queryset, many=True).data, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def followers(self, request, pk=None):
        try:
            obj = self.get_object()
            queryset = obj.followers.all()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = UserSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(
                UserSerializer(queryset, many=True).data, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def isfollowing(self, request, pk=None):
        try:
            obj = self.get_object()
            user = request.user
            if obj in user.following.all():
                return Response({"result": True})
            else:
                return Response({"result": False})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def isfollows(self, request, pk=None):
        try:
            obj = self.get_object()
            user = request.user
            if obj in user.followers.all():
                return Response({"result": True})
            else:
                return Response({"result": False})

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
                MovieSerializer(queryset, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def favorites(self, request, pk=None):
        try:
            obj = self.get_object()
            ct = ContentType.objects.get_for_model(Movie)
            q = obj.likes.filter(content_type=ct).values_list("object_id", flat=True)
            queryset = Movie.objects.filter(id__in=q)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = MovieSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(
                MovieSerializer(queryset, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
