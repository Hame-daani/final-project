from django.urls import path
from recommender.views import smView, suView, recommendationView

urlpatterns = [
    path("similar-movies/<int:pk>/", view=smView.as_view()),
    path("similar-users/", view=suView.as_view()),
    path("recommend/", view=recommendationView.as_view()),
]
