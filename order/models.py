from django.db import models


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        PREPARING = 'preparing', 'Preparing'
        READY = 'ready', 'Ready'
        PICKED_UP = 'picked_up', 'Picked Up'
        ON_THE_WAY = 'on_the_way', 'On the Way'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    order_id = models.CharField(max_length=255, unique=True, editable=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='orders')
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    courier = models.JSONField(null=True, blank=True, default=None)
    external_payment_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.subtotal + self.delivery_fee - self.discount + self.tip

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.order_id:
            self.order_id = f"order_{self.pk:03d}"
            Order.objects.filter(pk=self.pk).update(order_id=self.order_id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.SET_NULL, null=True, related_name="order_items")
    name = models.CharField(max_length=100)         # snapshot
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # snapshot
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # computed once at creation


class OrderItemAddon(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='addons')
    name = models.CharField(max_length=255)   # snapshot — no live FK to menu.Addon
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


class OrdersTimeLineEntry(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_timeline")
    status = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    time = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)