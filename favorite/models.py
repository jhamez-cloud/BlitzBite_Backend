from django.db import models

# Create your models here.
class Favorite(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name="favorites")
    restaurant = models.ForeignKey('restaurant.Restaurant',on_delete=models.CASCADE,related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)