from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

def get_default_preferences():
    return {
        "theme": "light",
        "notifications": {
            "email": True,
            "sms": False,
            "push": False
        },
    }

# Create your models here.
class User(AbstractUser):
    user_id = models.CharField(max_length=255, unique=True,editable=False)
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to='user/avatars/', null=True, blank=True)
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preferences = models.JSONField(default=get_default_preferences, blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self,*args, **kwargs):
        new = self.pk is None
        super().save(*args,**kwargs)

        if new and not self.user_id:
            self.user_id = f"user_{self.pk:03d}"
            User.objects.filter(pk=self.pk).update(user_id=self.user_id)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=255)
    address = models.TextField()  # the actual street address text — add if missing
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    @property
    def coordinates(self):
        if self.latitude is not None and self.longitude is not None:
            return (self.latitude, self.longitude)
        return None
    
class PaymentMethod(models.Model):
    class PaymentMethodType(models.TextChoices):
        CREDIT_CARD = 'credit card', 'Credit Card'
        DEBIT_CARD = 'debit card', 'Debit Card'
        PAYPAL = 'paypal', 'PayPal'
        APPLE_PAY = 'apple pay', 'Apple Pay'
        GOOGLE_PAY = 'google pay', 'Google Pay'
        BANK_TRANSFER = 'bank transfer', 'Bank Transfer'
        MOBILE_PAYMENT = 'mobile payment', 'Mobile Payment'
        Wallet = 'blitz wallet', 'Blitz Wallet'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    type = models.CharField(max_length=20, choices=PaymentMethodType.choices)
    label = models.CharField(max_length=255)
    details = models.JSONField(default=dict, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # worth adding, useful for ordering/display

    def save(self, *args, **kwargs):
        if self.is_default:
            PaymentMethod.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

