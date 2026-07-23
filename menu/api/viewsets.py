# menu/viewsets.py
from config.viewsets import StandardViewset
from menu.models import MenuCategory, MenuItem, MenuItemAddon, Addon
from menu.serializers import (
    MenuCategorySerializer,
    AddonSerializer,
    MenuItemListSerializer,
    MenuItemDetailSerializer,
    MenuItemWriteSerializer,
    MenuItemAddonSerializer,
    MenuItemAddonWriteSerializer,
)


class MenuCategoryViewSet(StandardViewset):
    """Top-level — categories aren't owned by a single restaurant,
    same reasoning as RestaurantCategory."""
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer


class AddonViewSet(StandardViewset):
    """Nested under restaurant — a restaurant's own reusable pool of extras."""
    serializer_class = AddonSerializer

    def get_queryset(self):
        return Addon.objects.filter(restaurant_id=self.kwargs['restaurant_pk'])

    def perform_create(self, serializer):
        serializer.save(restaurant_id=self.kwargs['restaurant_pk'])


class MenuItemViewSet(StandardViewset):
    """Nested under restaurant."""

    def get_serializer_class(self):
        if self.action == 'list':
            return MenuItemListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return MenuItemWriteSerializer
        return MenuItemDetailSerializer

    def get_queryset(self):
        qs = MenuItem.objects.filter(
            restaurant_id=self.kwargs['restaurant_pk']
        ).select_related('category')
        return qs

    def perform_create(self, serializer):
        serializer.save(restaurant_id=self.kwargs['restaurant_pk'])


class MenuItemAddonViewSet(StandardViewset):
    """Nested under menu item — which addons this specific item offers,
    and whether each is required/how many can be picked."""

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return MenuItemAddonWriteSerializer
        return MenuItemAddonSerializer

    def get_queryset(self):
        return MenuItemAddon.objects.filter(
            menu_item_id=self.kwargs['menuitem_pk']
        ).select_related('addon')

    def perform_create(self, serializer):
        serializer.save(menu_item_id=self.kwargs['menuitem_pk'])