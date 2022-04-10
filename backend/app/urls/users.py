from django.urls import path

from app.views.users import ProfileView

urlpatterns = [
    path("profile/<int:pk>/", view=ProfileView.as_view()),
]
