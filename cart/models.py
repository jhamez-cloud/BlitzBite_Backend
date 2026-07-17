from django.db import models
import uuid

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=255, unique=True, editable=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # auto calculated from cart items : price * quantity
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def total(self):
        return self.subtotal + self.delivery_fee - self.discount + self.tip
    
    def save(self,*args, **kwargs):
        new = self.pk is None
        super().save(*args,**kwargs)

        if new and not self.cart_id:
            self.cart_id = f"cart_{self.pk:03d}"
            Cart.objects.filter(pk=self.pk).update(cart_id=self.cart_id)

    def update_subtotal(self):
        subtotal = sum(item.subtotal for item in self.items.all())
        self.subtotal = subtotal
        self.save(update_fields=['subtotal'])

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE, related_name='cart_items')
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='cart_items')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selected_addons = models.ManyToManyField('menu.Addon', related_name='cart_items', blank=True)
    special_instructions = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)

        self.cart.update_subtotal()