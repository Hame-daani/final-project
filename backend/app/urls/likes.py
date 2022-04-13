from app.views.likes import LikeViewSet
from django.urls import path

urlpatterns = [path("<int:pk>/", view=LikeViewSet.as_view())]
