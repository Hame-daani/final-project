from django.urls import path

from app.views.auth import LogoutAPIView, UserRegistration, LoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path("register/", UserRegistration.as_view()),
]
