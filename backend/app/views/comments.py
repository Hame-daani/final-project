from rest_framework.viewsets import ModelViewSet

from app.models import Comment
from app.serializers import CommentSerializer
from app.permissions import isOwner
from app.mixins import Commentable, Likeable


class CommentViewSet(ModelViewSet, Commentable, Likeable):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (isOwner,)
