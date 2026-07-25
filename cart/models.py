from django.db import models
from decimal import Decimal
import uuid

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=255, unique=True, editable=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self,*args, **kwargs):
        new = self.pk is None
        super().save(*args,**kwargs)

        if new and not self.cart_id:
            self.cart_id = f"cart_{self.pk:03d}"
            Cart.objects.filter(pk=self.pk).update(cart_id=self.cart_id)

    @property
    def subtotal(self):
        return sum((item.subtotal for item in self.items.all()), Decimal('0.00'))

    @property
    def total(self):
        return self.subtotal + self.delivery_fee - self.discount + self.tip

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE, related_name='cart_items')
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='cart_items')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    selected_addons = models.ManyToManyField('menu.Addon', through='CartItemAddon', related_name='cart_items', blank=True)
    special_instructions = models.TextField(null=True, blank=True)

    @property
    def subtotal(self):
        addon_total = sum(
            (cart_item.price * cart_item.quantity for cart_item in self.cartitemaddon_set.all()),
            Decimal('0.00')
        )
        return (self.price * self.quantity) + addon_total


class CartItemAddon(models.Model):
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    addon = models.ForeignKey('menu.Addon', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot, same reasoning as CartItem.price

    class Meta:
        unique_together = ('cart_item', 'addon')