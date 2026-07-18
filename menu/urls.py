from rest_framework.routers import DefaultRouter
from .api.viewsets import MenuItemViewset

router = DefaultRouter()
router.register(r"menu-items",MenuItemViewset,basename="menu-items")

urlpatterns = router.urls