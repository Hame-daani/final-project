from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from app.models import Review
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
        obj = Review(user=request.user)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
