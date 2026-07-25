# cart/serializers.py
from decimal import Decimal
from rest_framework import serializers
from menu.models import MenuItem, Addon, MenuItemAddon
from .models import Cart, CartItem, CartItemAddon


class CartItemAddonSerializer(serializers.ModelSerializer):
    """Read-side: flattens addon name alongside the selected quantity/price snapshot."""
    addon_id = serializers.IntegerField(source='addon.id', read_only=True)
    name = serializers.CharField(source='addon.name', read_only=True)

    class Meta:
        model = CartItemAddon
        fields = ['addon_id', 'name', 'price', 'quantity']
        read_only_fields = ['price']  # snapshot — set server-side, never client-writable


class CartItemAddonWriteSerializer(serializers.Serializer):
    """Used inside CartItemWriteSerializer's nested input — just addon id + quantity,
    price snapshot and validation happen server-side."""
    addon_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class CartItemSerializer(serializers.ModelSerializer):
    """Read-side representation of a cart item, including computed subtotal
    and its selected addons with quantities."""
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    selected_addons = CartItemAddonSerializer(source='cartitemaddon_set', many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'menu_item', 'restaurant', 'name', 'price', 'quantity',
            'subtotal', 'selected_addons', 'special_instructions',
        ]
        read_only_fields = ['id', 'restaurant', 'name', 'price']
        # name/price are snapshotted server-side from menu_item at creation time,
        # never accepted directly from the client


class CartItemWriteSerializer(serializers.ModelSerializer):
    """Used for add-to-cart / update-quantity requests. Client sends menu_item_id,
    quantity, addon selections (with quantities), and instructions — everything
    else (name, price, restaurant) is derived server-side from the live MenuItem."""
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    selected_addons = CartItemAddonWriteSerializer(many=True, required=False)

    class Meta:
        model = CartItem
        fields = ['menu_item', 'quantity', 'selected_addons', 'special_instructions']

    def validate(self, attrs):
        menu_item = attrs['menu_item']

        if not menu_item.available:
            raise serializers.ValidationError({'menu_item': 'This item is currently unavailable.'})

        # Re-validate addon selections against what THIS menu item actually offers,
        # including is_required / max_selectable rules from MenuItemAddon.
        offered = {
            mia.addon_id: mia
            for mia in MenuItemAddon.objects.filter(menu_item=menu_item)
        }
        selected = attrs.get('selected_addons', [])
        selected_ids = set()

        for entry in selected:
            addon_id = entry['addon_id']
            quantity = entry['quantity']
            rule = offered.get(addon_id)

            if rule is None:
                raise serializers.ValidationError({
                    'selected_addons': f"Addon {addon_id} is not offered on this menu item."
                })
            if quantity > rule.max_selectable:
                raise serializers.ValidationError({
                    'selected_addons': f"Addon {addon_id} allows at most {rule.max_selectable}."
                })
            selected_ids.add(addon_id)

        missing_required = [
            mia.addon_id for mia in offered.values()
            if mia.is_required and mia.addon_id not in selected_ids
        ]
        if missing_required:
            raise serializers.ValidationError({
                'selected_addons': f"Required addon(s) missing: {missing_required}"
            })

        return attrs

    def create(self, validated_data):
        selected_addons_data = validated_data.pop('selected_addons', [])
        menu_item = validated_data['menu_item']

        cart_item = CartItem.objects.create(
            cart=self.context['cart'],
            menu_item=menu_item,
            restaurant=menu_item.restaurant,
            name=menu_item.name,          # snapshot at add-time
            price=menu_item.price,        # snapshot at add-time
            quantity=validated_data.get('quantity', 1),
            special_instructions=validated_data.get('special_instructions'),
        )

        addon_lookup = {a.id: a for a in Addon.objects.filter(
            id__in=[e['addon_id'] for e in selected_addons_data]
        )}
        CartItemAddon.objects.bulk_create([
            CartItemAddon(
                cart_item=cart_item,
                addon=addon_lookup[entry['addon_id']],
                quantity=entry['quantity'],
                price=addon_lookup[entry['addon_id']].price,  # snapshot
            )
            for entry in selected_addons_data
        ])

        return cart_item


class CartSerializer(serializers.ModelSerializer):
    """Read-only representation of the full cart — items and computed totals."""
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 'cart_id', 'items', 'subtotal',
            'delivery_fee', 'discount', 'tip', 'total',
        ]
        read_only_fields = ['id', 'cart_id', 'subtotal', 'total']