print("user urls loaded")
from rest_framework.routers import DefaultRouter
from .api.viewsets import UserViewset

router = DefaultRouter()
router.register(r"user", UserViewset, basename="users")

urlpatterns = router.urls