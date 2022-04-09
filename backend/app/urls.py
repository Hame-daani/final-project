from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token

from .views import LogoutAPIView, UserRegistration

urlpatterns = [
    path("login/", view=obtain_auth_token),
    path("logout/", view=LogoutAPIView.as_view()),
    path("register/", UserRegistration.as_view()),
]
