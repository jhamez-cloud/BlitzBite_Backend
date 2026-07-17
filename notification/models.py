from django.db import models

# Create your models here.
class Notification(models.Model):
    class NotificationType(models.TextChoices):
        ORDER_UPDATE = 'order_update', 'Order Update'
        PROMOTION = 'promotion', 'Promotion'
        SYSTEM = 'system', 'System'
        REVIEW = 'review', 'Review'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50, choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)