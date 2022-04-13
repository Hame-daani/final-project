from rest_framework.generics import DestroyAPIView

from app.models import Like
from app.serializers import LikeSerializer
from app.permissions import isOwner


class LikeViewSet(DestroyAPIView):

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (isOwner,)
