from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from app.models import Comment
from app.serializers import CommentSerializer
from app.permissions import isOwner
from app.mixins import Commentable, Likeable


class CommentViewSet(ModelViewSet, Commentable, Likeable):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (isOwner,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["user"]
    ordering_fields = ["created_at"]
