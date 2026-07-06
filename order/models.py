from django.db import models

def get_courier_details():
    return {
        "name": "",
        "phone": "",
        "vehicle": "",
        "license_plate": "",
    }

# Create your models here.
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
    user = models.ForeignKey('user.User', 
                             on_delete=models.CASCADE, 
                             related_name='orders',
                             null=True, 
                             blank=True
                            )
    restaurant = models.ForeignKey('restaurant.Restaurant',
                                   on_delete=models.CASCADE,
                                   related_name='orders'
                                  )
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    courier = models.JSONField(default=get_courier_details, blank=True)
    external_payment_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        new = self.pk is None
        super().save(*args,**kwargs)

        if new and not self.order_id:
            self.order_id = f"order_{self.pk:03d}"
            Order.objects.filter(pk=self.pk).update(order_id=self.order_id)

    def update_subtotal(self):
        subtotal = sum(item.subtotal for item in self.order_items.all())
        self.subtotal = subtotal
        self.save(update_fields=["subtotal"])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, 
                              on_delete=models.CASCADE, 
                              related_name='order_items'
                              )
    menu_item = models.ForeignKey('menu.MenuItem',
                                  on_delete=models.CASCADE,
                                  related_name="order_items")
    addons = models.ForeignKey('menu.Addons',
                               on_delete=models.CASCADE,
                               related_name="order_items")
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self,*args,**kwargs):
        self.subtotal = (self.quantity * self.price) + self.addons.price
        super().save(*args,**kwargs)

        self.order.update_subtotal()