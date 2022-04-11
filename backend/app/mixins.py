from rest_framework.decorators import action
from rest_framework.response import Response
from app.serializers import CommentSerializer
from rest_framework import status


class Commentable:
    @action(detail=True, methods=["POST", "GET"])
    def comments(self, request, pk=None):
        if request.method == "POST":
            try:
                obj = self.get_object()
                obj.comments.create(user=request.user, text=request.data["text"])
                c = obj.comments.last()
                return Response(
                    CommentSerializer(c).data, status=status.HTTP_201_CREATED
                )
            except:
                return Response(
                    {"error": "make sure to send a text"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if request.method == "GET":
            obj = self.get_object()
            return Response(
                CommentSerializer(obj.comments.all(), many=True).data,
                status=status.HTTP_200_OK,
            )
