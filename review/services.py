# reviews/services.py
from django.db import transaction
from django.db.models import Avg, Count
from .models import Review


def recalculate_restaurant_rating(restaurant):
    aggregates = Review.objects.filter(restaurant=restaurant).aggregate(
        avg_rating=Avg('rating'), count=Count('id')
    )
    restaurant.rating = aggregates['avg_rating'] or 0
    restaurant.review_count = aggregates['count']
    restaurant.save(update_fields=['rating', 'review_count'])


@transaction.atomic
def create_review(user, order, rating, comment=None):
    if order.user_id != user.id:
        raise ValueError("You can only review your own orders.")

    if order.status != order.OrderStatus.DELIVERED:
        raise ValueError("You can only review an order after it has been delivered.")

    if Review.objects.filter(user=user, order=order).exists():
        raise ValueError("You have already reviewed this order.")

    review = Review.objects.create(
        user=user,
        restaurant=order.restaurant,
        order=order,
        rating=rating,
        comment=comment,
    )

    recalculate_restaurant_rating(order.restaurant)

    return review