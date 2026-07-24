# restaurants/urls.py — becomes the single source of truth for anything nested under restaurant
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .api.viewsets import RestaurantViewSet, OpeningHoursViewSet, RestaurantCategoryViewSet
from menu.api.viewsets import AddonViewSet, MenuItemViewSet, MenuItemAddonViewSet

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")
router.register(r"restaurant-categories", RestaurantCategoryViewSet, basename="restaurant-categories")

restaurants_router = routers.NestedSimpleRouter(router, r"restaurants", lookup="restaurant")
restaurants_router.register(r"opening-hours", OpeningHoursViewSet, basename="restaurant-opening-hours")
restaurants_router.register(r"addons", AddonViewSet, basename="restaurant-addons")
restaurants_router.register(r"menu-items", MenuItemViewSet, basename="restaurant-menu-items")

menu_items_router = routers.NestedSimpleRouter(restaurants_router, r"menu-items", lookup="menuitem")
menu_items_router.register(r"addon-options", MenuItemAddonViewSet, basename="menuitem-addon-options")

urlpatterns = router.urls + restaurants_router.urls + menu_items_router.urls