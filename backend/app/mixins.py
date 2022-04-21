from rest_framework.decorators import action
from rest_framework.response import Response
from app.serializers import (
    CommentSerializer,
    LikeSerializer,
    MovieSerializer,
)
from rest_framework import status


class Commentable:
    @action(detail=True, methods=["POST", "GET"])
    def comments(self, request, pk=None):
        if request.method == "POST":
            try:
                obj = self.get_object()
                obj.comments.create(user=request.user, text=request.data.get("text"))
                c = obj.comments.last()
                return Response(
                    CommentSerializer(c).data, status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if request.method == "GET":
            obj = self.get_object()
            queryset = obj.comments.all()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = CommentSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(
                CommentSerializer(obj.comments.all(), many=True).data,
                status=status.HTTP_200_OK,
            )


class Likeable:
    @action(detail=True, methods=["POST", "GET", "DELETE"])
    def likes(self, request, pk=None):
        if request.method == "POST":
            try:
                obj = self.get_object()
                obj.likes.create(user=request.user)
                c = obj.likes.last()
                return Response(LikeSerializer(c).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if request.method == "GET":
            obj = self.get_object()
            # q = User.objects.filter(
            #     pk__in=obj.likes.all().values_list("user", flat=True)
            # )
            q = obj.likes.all()
            return Response(
                LikeSerializer(q, many=True).data,
                status=status.HTTP_200_OK,
            )
        if request.method == "DELETE":
            try:
                obj = self.get_object()
                obj.likes.filter(user=request.user).delete()
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
