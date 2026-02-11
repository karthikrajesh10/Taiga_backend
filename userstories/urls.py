# userstories/urls.py
from rest_framework.routers import DefaultRouter
from .views import UserStoryViewSet

router = DefaultRouter()
router.register(r"userstories", UserStoryViewSet, basename="userstory")

urlpatterns = router.urls
