from app.views.comments import CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", CommentViewSet, basename="comment")
urlpatterns = router.urls
