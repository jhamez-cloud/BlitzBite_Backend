# orders/services.py
from decimal import Decimal
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from promotion.models import Coupon
from .models import Order, OrderItem, OrderItemAddon, OrdersTimeLineEntry


def _apply_coupon(coupon_code, subtotal):
    """Validates the coupon and atomically consumes one use of it.
    Returns the discount amount, or raises ValueError if invalid.
    Must be called inside the same transaction as order creation, so a
    failed order never leaves a coupon partially consumed."""
    try:
        coupon = Coupon.objects.select_for_update().get(code__iexact=coupon_code)
    except Coupon.DoesNotExist:
        raise ValueError(f"Coupon '{coupon_code}' not found.")

    if not coupon.is_valid_now:
        raise ValueError(f"Coupon '{coupon_code}' is no longer valid.")

    if subtotal < coupon.minimum_order:
        raise ValueError(
            f"Order must be at least {coupon.minimum_order} to use coupon '{coupon_code}'."
        )

    # Atomic increment — only succeeds if usage limit hasn't been reached.
    # Guards against two concurrent checkouts both consuming the last use.
    updated = Coupon.objects.filter(
        pk=coupon.pk, used_count__lt=F('max_uses')
    ).update(used_count=F('used_count') + 1)

    if not updated:
        raise ValueError(f"Coupon '{coupon_code}' has reached its usage limit.")

    if coupon.discount_type == Coupon.DiscountTypes.PERCENTAGE:
        discount = subtotal * (coupon.discount_value / 100)
    else:
        discount = coupon.discount_value

    return min(discount, subtotal)  # never discount below zero


@transaction.atomic
def create_order_from_cart(cart, user, delivery_address, payment_method, tip=Decimal('0.00'), coupon_code=None):
    if not cart.items.exists():
        raise ValueError("Cannot create an order from an empty cart.")

    restaurant = cart.items.first().restaurant

    for cart_item in cart.items.all():
        live_item = cart_item.menu_item
        if not live_item.available:
            raise ValueError(f"'{live_item.name}' is no longer available.")

    subtotal = cart.subtotal
    discount = Decimal('0.00')

    if coupon_code:
        discount = _apply_coupon(coupon_code, subtotal)
        # If _apply_coupon raises ValueError, @transaction.atomic rolls back
        # everything — no order is created, and the coupon's used_count
        # increment above is undone too, since it's all one transaction.

    order = Order.objects.create(
        user=user,
        restaurant=restaurant,
        subtotal=subtotal,
        delivery_fee=cart.delivery_fee,
        discount=discount,
        tip=tip,
        delivery_address=delivery_address,
        payment_method=payment_method,
        status=Order.OrderStatus.PENDING,
    )

    for cart_item in cart.items.all():
        order_item = OrderItem.objects.create(
            order=order,
            menu_item=cart_item.menu_item,
            name=cart_item.name,
            price=cart_item.price,
            quantity=cart_item.quantity,
            subtotal=cart_item.subtotal,
        )
        OrderItemAddon.objects.bulk_create([
            OrderItemAddon(
                order_item=order_item,
                name=ca.addon.name,
                price=ca.price,
                quantity=ca.quantity,
            )
            for ca in cart_item.cartitemaddon_set.all()
        ])

    OrdersTimeLineEntry.objects.create(
        order=order,
        status=Order.OrderStatus.PENDING,
        label='Order placed',
        time=timezone.now(),
        completed=True,
    )

    cart.items.all().delete()

    return order