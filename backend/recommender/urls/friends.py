from django.urls import path
from recommender.views import FriendsRecommendationView

urlpatterns = [
    path("recommend/", view=FriendsRecommendationView.as_view()),
]
