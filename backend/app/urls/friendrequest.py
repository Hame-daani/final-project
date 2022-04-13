from app.views.friendrequest import FrView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", FrView, basename="friendrequest")
urlpatterns = router.urls
