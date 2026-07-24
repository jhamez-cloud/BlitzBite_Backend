from datetime import datetime
from django.db import models
from django.utils.text import slugify
from config.helpers import generate_unique_slug

# Create your models here.
class Restaurant(models.Model):
    restaurant_id = models.CharField(max_length=255, unique=True, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='restaurant/logos/', null=True, blank=True)
    banner = models.ImageField(upload_to='restaurant/banners/', null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    delivery_time_min = models.PositiveIntegerField(help_text="Estimated Minimum Delivery Time in minutes")
    delivery_time_max = models.PositiveIntegerField(help_text="Estimated Maximum Delivery Time in minutes")
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    categories = models.ManyToManyField('RestaurantCategory', related_name='restaurants')
    is_temporarily_closed = models.BooleanField(default=False, help_text="Manual override — restaurant paused even during normal hours")
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    description = models.TextField()
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_open_now(self):
        now = datetime.now()
        today = now.weekday()  # matches OpeningHours.Weekday (Monday=0)
        current_time = now.time()

        hours_today = self.opening_hours.filter(day=today).first()
        if not hours_today:
            return False  # no hours defined for today = closed

        return hours_today.open_time <= current_time <= hours_today.close_time

    def save(self,*args, **kwargs):
        new = self.pk is None
        super().save(*args,**kwargs)
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        
        if new and not self.restaurant_id:
            self.restaurant_id = f"restaurant_{self.pk:03d}"
            self.slug = slugify(self.name)
            Restaurant.objects.filter(pk=self.pk).update(
                restaurant_id=self.restaurant_id, 
                slug=self.slug
            )

class OpeningHours(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'
        SATURDAY = 5, 'Saturday'
        SUNDAY = 6, 'Sunday'

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='opening_hours'
    )
    day = models.IntegerField(choices=Weekday.choices)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        unique_together = ('restaurant', 'day')
        ordering = ['day']

class RestaurantCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='restaurant/categories/', null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
            RestaurantCategory.objects.filter(pk=self.pk).update(slug=self.slug)

    def __str__(self):
        return f"Category-{self.id}: {self.name}"

