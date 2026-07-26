# orders/services.py
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import Order, OrderItem, OrderItemAddon, OrdersTimeLineEntry


@transaction.atomic
def create_order_from_cart(cart, user, delivery_address, payment_method, tip=Decimal('0.00'), coupon_code=None):
    if not cart.items.exists():
        raise ValueError("Cannot create an order from an empty cart.")

    # All items in a cart are assumed to belong to one restaurant (per your
    # spec's single-restaurant-per-cart constraint) — take it from the first item.
    restaurant = cart.items.first().restaurant

    # Re-validate live prices/availability at checkout — never trust the cart's
    # cached snapshot for the actual charge (per your original business rules).
    for cart_item in cart.items.all():
        live_item = cart_item.menu_item
        if not live_item.available:
            raise ValueError(f"'{live_item.name}' is no longer available.")

    discount = Decimal('0.00')
    # TODO: real coupon validation/application happens once the promotions app exists.
    # For now, coupon_code is accepted but not yet applied.

    order = Order.objects.create(
        user=user,
        restaurant=restaurant,
        subtotal=cart.subtotal,
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

    # Clear the cart now that it's been converted into an order
    cart.items.all().delete()

    return order