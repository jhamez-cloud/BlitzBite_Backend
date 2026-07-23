import uuid
from django.db import models
from django.core.validators import MinValueValidator
from config.helpers import generate_unique_slug

# Create your models here.
class MenuCategory(models.Model):
    category_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)

        super().save(*args,**kwargs)

class MenuItem(models.Model):
    item_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(MenuCategory, on_delete=models.PROTECT, null=True, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    image = models.ImageField(upload_to='menu/items/', null=True, blank=True)
    available = models.BooleanField(default=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    is_popular = models.BooleanField(default=False)
    addons = models.ManyToManyField('Addon', through='MenuItemAddon', related_name='menu_items', blank=True)

class MenuItemAddon(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    addon = models.ForeignKey('Addon', on_delete=models.CASCADE)
    is_required = models.BooleanField(default=False)
    max_selectable = models.PositiveIntegerField(
        default=1, help_text="Max quantity of this addon a customer can select"
    )

    class Meta:
        unique_together = ('menu_item', 'addon')

class Addon(models.Model):
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='addons')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])