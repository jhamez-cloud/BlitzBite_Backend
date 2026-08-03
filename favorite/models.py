from django.db import models
class Favorite(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name="favorites")
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')
        ordering = ['-created_at']