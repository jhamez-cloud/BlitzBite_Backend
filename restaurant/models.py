from django.db import models
from django.utils.text import slugify
# Create your models here.
class Restaurant(models.Model):
    restaurant_id = models.CharField(max_length=255, unique=True, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='restaurant/logos/', null=True, blank=True)
    banner = models.ImageField(upload_to='restaurant/banners/', null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    delivery_time = models.CharField(max_length=255)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    categories = models.ManyToManyField('RestaurantCategory', related_name='restaurants')
    is_open = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    description = models.TextField()
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args, **kwargs):
        new = self.pk is None
        super().save(*args,**kwargs)

        if new and not self.restaurant_id and not self.slug:
            self.restaurant_id = f"restaurant_{self.pk:03d}"
            self.slug = slugify(self.name)
            Restaurant.objects.filter(pk=self.pk).update(
                restaurant_id=self.restaurant_id, 
                slug=self.slug
            )

class OpeningHours(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='opening_hours')
    day = models.CharField(max_length=10)
    open_time = models.TimeField()
    close_time = models.TimeField()

class RestaurantCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='restaurant/categories/', null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        if not self.slug:
            self.slug = slugify(self.name)
            RestaurantCategory.objects.filter(pk=self.pk).update(slug=self.slug)

