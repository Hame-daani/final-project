from app.views.reviews import ReviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", ReviewViewSet, basename="review")
urlpatterns = router.urls
