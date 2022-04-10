from app.models import User
from rest_framework.generics import RetrieveUpdateAPIView
from app.permissions import isSelf

from app.serializers import UserSerializer


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (isSelf,)
    queryset = User.objects.all()
