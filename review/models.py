from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'order')
        ordering = ['-date']