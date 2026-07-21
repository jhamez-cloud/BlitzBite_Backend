# restaurants/urls.py
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .api.viewsets import RestaurantViewSet, OpeningHoursViewSet, RestaurantCategoryViewSet

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")
router.register(r"restaurant-categories", RestaurantCategoryViewSet, basename="restaurant-categories")

restaurants_router = routers.NestedSimpleRouter(router, r"restaurants", lookup="restaurant")
restaurants_router.register(r"opening-hours", OpeningHoursViewSet, basename="restaurant-opening-hours")

urlpatterns = router.urls + restaurants_router.urls