from django.urls import path, include


urlpatterns = [
    path("auth/", include("app.urls.auth")),
    path("users/", include("app.urls.users")),
    path("movies/", include("app.urls.movies")),
    path("reviews/", include("app.urls.reviews")),
    path("comments/", include("app.urls.comments")),
    path("likes/", include("app.urls.likes")),
    path("fr/", include("app.urls.friendrequest")),
]
