# restaurants/viewsets.py
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from config.viewsets import StandardViewset  # your existing wrapper base
from restaurant.models import Restaurant, OpeningHours, RestaurantCategory
from restaurant.serializers import (
    RestaurantListSerializer,
    RestaurantDetailSerializer,
    RestaurantWriteSerializer,
    OpeningHoursSerializer,
    RestaurantCategorySerializer,
)


class RestaurantViewSet(StandardViewset):
    queryset = Restaurant.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_featured', 'is_trending', 'is_temporarily_closed', 'categories']
    search_fields = ['name', 'description', 'address']

    def get_serializer_class(self):
        if self.action == 'list':
            return RestaurantListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return RestaurantWriteSerializer
        return RestaurantDetailSerializer

    def get_queryset(self):
        qs = Restaurant.objects.prefetch_related('categories')
        if self.action == 'retrieve':
            qs = qs.prefetch_related('opening_hours')
        return qs


class OpeningHoursViewSet(StandardViewset):
    serializer_class = OpeningHoursSerializer

    def get_queryset(self):
        return OpeningHours.objects.filter(restaurant_id=self.kwargs['restaurant_pk'])

    def perform_create(self, serializer):
        serializer.save(restaurant_id=self.kwargs['restaurant_pk'])


class RestaurantCategoryViewSet(StandardViewset):
    queryset = RestaurantCategory.objects.all()
    serializer_class = RestaurantCategorySerializer