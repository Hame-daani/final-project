from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from app.serializers import UserSerializer


class LogoutAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={"message": f"Bye {request.user.username}!"})


class UserRegistration(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
