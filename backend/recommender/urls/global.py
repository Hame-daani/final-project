from django.urls import path
from recommender.views import smView, suView, GlobalRecommendationView

urlpatterns = [
    path("similar-movies/<int:pk>/", view=smView.as_view()),
    path("similar-users/", view=suView.as_view()),
    path("recommend/", view=GlobalRecommendationView.as_view()),
]
