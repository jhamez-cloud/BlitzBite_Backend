from django.db import models

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        ORDER_UPDATE = 'order_update', 'Order Update'
        PROMOTION = 'promotion', 'Promotion'
        SYSTEM = 'system', 'System'
        REVIEW = 'review', 'Review'

    ICON_MAP = {
        NotificationType.ORDER_UPDATE: 'ShoppingCart',
        NotificationType.PROMOTION: 'TicketPercent',
        NotificationType.SYSTEM: 'Settings',
        NotificationType.REVIEW: 'Star',
    }

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50, choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(max_length=500, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-time']

    @property
    def icon(self):
        return self.ICON_MAP.get(self.type, 'Bell')