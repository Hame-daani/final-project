from app.views.movies import MovieViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", MovieViewSet, basename="movie")
urlpatterns = router.urls
