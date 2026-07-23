# menu/serializers.py
from rest_framework import serializers
from .models import MenuCategory, MenuItem, MenuItemAddon, Addon


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['id', 'category_id', 'name', 'slug']
        read_only_fields = ['id', 'category_id', 'slug']


class AddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = ['id', 'name', 'price']
        read_only_fields = ['id']
        # 'restaurant' excluded — set server-side from the URL, same pattern as OpeningHours


class MenuItemAddonSerializer(serializers.ModelSerializer):
    """Represents one addon *as offered on a specific menu item* — includes
    the addon's own name/price plus the per-item rules (required, max_selectable)."""
    id = serializers.IntegerField(source='addon.id', read_only=True)
    name = serializers.CharField(source='addon.name', read_only=True)
    price = serializers.DecimalField(source='addon.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = MenuItemAddon
        fields = ['id', 'name', 'price', 'is_required', 'max_selectable']


class MenuItemAddonWriteSerializer(serializers.ModelSerializer):
    """Used when attaching/updating which addons apply to a menu item —
    takes an addon id directly rather than nested addon data."""
    addon = serializers.PrimaryKeyRelatedField(queryset=Addon.objects.all())

    class Meta:
        model = MenuItemAddon
        fields = ['addon', 'is_required', 'max_selectable']

    def validate(self, attrs):
        if attrs.get('max_selectable', 1) < 1:
            raise serializers.ValidationError("max_selectable must be at least 1.")
        return attrs


class MenuItemListSerializer(serializers.ModelSerializer):
    """Lightweight version for browsing a restaurant's full menu grid."""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id', 'item_id', 'name', 'price', 'image',
            'category', 'available', 'is_popular',
        ]
        read_only_fields = ['id', 'item_id']


class MenuItemDetailSerializer(serializers.ModelSerializer):
    """Full version for a single item's page — includes description,
    calories, and the complete addon list with per-item rules."""
    category = MenuCategorySerializer(read_only=True)
    addon_options = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = [
            'id', 'item_id', 'restaurant', 'name', 'description', 'price',
            'image', 'category', 'available', 'calories', 'is_popular',
            'addon_options',
        ]
        read_only_fields = ['id', 'item_id', 'restaurant']

    def get_addon_options(self, obj):
        # Goes through MenuItemAddon (not obj.addons directly) so we get the
        # per-item is_required/max_selectable rules alongside each addon.
        through_rows = MenuItemAddon.objects.filter(menu_item=obj).select_related('addon')
        return MenuItemAddonSerializer(through_rows, many=True).data


class MenuItemWriteSerializer(serializers.ModelSerializer):
    """Used for create/update — 'restaurant' and 'category' by id,
    availability/pricing directly writable, addons managed separately
    via the MenuItemAddon nested endpoint, not through this serializer."""

    class Meta:
        model = MenuItem
        fields = [
            'name', 'description', 'price', 'image', 'category',
            'available', 'calories', 'is_popular',
        ]
        # 'restaurant' excluded — set server-side from the URL (nested under restaurant)

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("price cannot be negative.")
        return value