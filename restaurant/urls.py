from rest_framework.routers import DefaultRouter
from .api.viewsets import RestaurantViewset

router = DefaultRouter()
router.register(r"restaurant", RestaurantViewset, basename="restaurants")

urlpatterns = router.urls