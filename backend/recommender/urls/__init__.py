from django.urls import path, include


urlpatterns = [
    path("global/", include("recommender.urls.global")),
    path("friends/", include("recommender.urls.friends")),
]
