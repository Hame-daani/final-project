from django.urls import path
from recommender.views import smView

urlpatterns = [
    path("similar-movies/<int:pk>/", view=smView.as_view()),
]
