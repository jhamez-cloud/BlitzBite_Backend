# reviews/urls.py — nested under restaurants, so lives alongside that router
from rest_framework_nested import routers
from restaurant.urls import router as restaurants_router  # reuse the already-registered 'restaurants' prefix
from review.api.viewsets import RestaurantReviewViewSet

reviews_router = routers.NestedSimpleRouter(restaurants_router, r"restaurants", lookup="restaurant")
reviews_router.register(r"reviews", RestaurantReviewViewSet, basename="restaurant-reviews")

urlpatterns = reviews_router.urls