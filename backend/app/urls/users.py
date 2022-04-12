from django.urls import path

from app.views.users import ProfileView, FriendsView

urlpatterns = [
    path("<int:pk>/profile/", view=ProfileView.as_view()),
    path("<int:pk>/friends/", view=FriendsView.as_view()),
]
