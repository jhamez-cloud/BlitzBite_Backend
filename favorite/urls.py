from rest_framework.routers import DefaultRouter
from .api.viewsets import FavoriteViewset

router = DefaultRouter()
router.register(r"favorites",FavoriteViewset,basename="favorites")

urlpatterns = router.urls