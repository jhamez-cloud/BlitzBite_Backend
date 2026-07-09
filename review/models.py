from django.db import models

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)