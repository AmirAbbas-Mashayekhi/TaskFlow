from rest_framework.routers import DefaultRouter
from .views import ParticipantViewSet

router = DefaultRouter()
router.register('participants', ParticipantViewSet, basename='participants')
# TODO: Create Team Route

urlpatterns = router.urls
