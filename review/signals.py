# reviews/signals.py
from django.db.models import Avg, Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review


def recalculate_restaurant_rating(restaurant):
    stats = restaurant.reviews.aggregate(avg=Avg('rating'), count=Count('id'))
    restaurant.rating = round(stats['avg'] or 0, 1)
    restaurant.review_count = stats['count']
    restaurant.save(update_fields=['rating', 'review_count'])


@receiver(post_save, sender=Review)
def on_review_saved(sender, instance, **kwargs):
    recalculate_restaurant_rating(instance.restaurant)


@receiver(post_delete, sender=Review)
def on_review_deleted(sender, instance, **kwargs):
    recalculate_restaurant_rating(instance.restaurant)