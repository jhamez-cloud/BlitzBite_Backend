from rest_framework.routers import DefaultRouter
from .api.viewsets import ReviewViewset

router = DefaultRouter()
router.register(r"reviews",ReviewViewset,basename="reviews")

urlpatterns = router.urls