from django.db import models

# Create your models here.
class Promotion(models.Model):
    promotion_id = models.CharField(max_length=255, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    code = models.CharField(max_length=50, unique=True,null=True, blank=True)
    image = models.ImageField(upload_to='promotions/', null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    background_color = models.CharField(max_length=7, default='#FFFFFF')  # Default white background
    text_color = models.CharField(max_length=7, default='#000000')  # Default black text
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        new = self.pk is None
        super().save(*args, **kwargs)

        if new and not self.promotion_id:
            self.promotion_id = f"promo_{self.pk:03d}"
            Promotion.objects.filter(pk=self.pk).update(promotion_id=self.promotion_id)

class Coupon(models.Model):
    class DiscountTypes(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        FIXED_AMOUNT = 'fixed_amount', 'Fixed Amount'

    coupon_id = models.CharField(max_length=255, unique=True, editable=False)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_type = models.CharField(max_length=20, choices=DiscountTypes.choices,default=DiscountTypes.PERCENTAGE)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valid_until = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)
    max_uses = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        new = self.pk is None
        super().save(*args, **kwargs)

        if new and not self.coupon_id:
            self.coupon_id = f"coupon_{self.pk:03d}"
            Coupon.objects.filter(pk=self.pk).update(coupon_id=self.coupon_id)
