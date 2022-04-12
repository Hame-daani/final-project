from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend

from app.models import FriendRequest, User
from app.serializers import FrSerializer
from app.permissions import FrPermission


class FrView(ModelViewSet):
    serializer_class = FrSerializer
    permission_classes = (FrPermission,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["from_user", "to_user"]
    ordering = ["date"]

    def get_queryset(self):
        u = self.request.user
        return FriendRequest.objects.filter(Q(to_user=u) | Q(from_user=u))

    def create(self, request, *args, **kwargs):
        try:
            s = request.user
            r = User.objects.get(id=request.data["to"])
            obj = FriendRequest(from_user=s, to_user=r)
            serializer = self.serializer_class(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"])
    def accept(self, request, pk=None):
        obj = self.get_object()
        if obj.status == "p":
            obj.status = "a"
            return Response({"status": "accepted"}, status=status.HTTP_200_OK)
        if obj.status == "r":
            return Response(
                {"status": "already rejected"}, status=status.HTTP_409_CONFLICT
            )
        if obj.status == "a":
            return Response(
                {"status": "already accepted"}, status=status.HTTP_409_CONFLICT
            )

    @action(detail=True, methods=["POST"])
    def reject(self, request, pk=None):
        obj = self.get_object()
        if obj.status == "p":
            obj.status = "r"
            return Response({"status": "rejected"}, status=status.HTTP_200_OK)
        if obj.status == "a":
            return Response(
                {"status": "already accepted"}, status=status.HTTP_409_CONFLICT
            )
        if obj.status == "r":
            return Response(
                {"status": "already rejected"}, status=status.HTTP_409_CONFLICT
            )

    def update(self, request, pk=None):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
