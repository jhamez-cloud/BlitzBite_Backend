from rest_framework.routers import DefaultRouter
from .api.viewsets import NotificationViewset

router = DefaultRouter()
router.register(r"notifications",NotificationViewset,basename="notifications")

urlpatterns = router.urls