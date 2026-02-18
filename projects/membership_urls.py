from rest_framework.routers import DefaultRouter
from .views import ProjectMembershipViewSet

router = DefaultRouter()
router.register(r"", ProjectMembershipViewSet, basename="membership")

urlpatterns = router.urls
