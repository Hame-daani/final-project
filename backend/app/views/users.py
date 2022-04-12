from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from app.models import User
from app.permissions import isSelf
from app.serializers import UserSerializer


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (isSelf,)
    queryset = User.objects.all()


class FriendsView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, pk=None):
        try:
            obj = self.get_object()
            return Response(
                UserSerializer(obj.friends.all(), many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
