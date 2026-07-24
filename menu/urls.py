# menu/urls.py — only owns the truly top-level, non-nested route
from rest_framework.routers import DefaultRouter
from .api.viewsets import MenuCategoryViewSet

router = DefaultRouter()
router.register(r"menu-categories", MenuCategoryViewSet, basename="menu-categories")

urlpatterns = router.urls