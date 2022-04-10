from django.urls import path, include


urlpatterns = [
    path("auth/", include("app.urls.auth")),
    path("users/", include("app.urls.users")),
]
