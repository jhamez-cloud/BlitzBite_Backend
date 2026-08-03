# favorites/urls.py
from rest_framework.routers import DefaultRouter
from .api.viewsets import FavoriteViewSet

router = DefaultRouter()
router.register(r"users/me/favorites", FavoriteViewSet, basename="favorites")

urlpatterns = router.urls