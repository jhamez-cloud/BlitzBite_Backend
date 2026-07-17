from django.db import models
from django.utils.text import slugify

# Create your models here.
class MenuCategory(models.Model):
    category_id = models.CharField(max_length=255, unique=True, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self,*args, **kwargs):
        new = self.pk is None
        super().save(*args,**kwargs)

        if new and not self.category_id and not self.slug:
            self.category_id = f"menu_category_{self.pk:03d}"
            self.slug = slugify(self.name)
            MenuCategory.objects.filter(pk=self.pk).update(
                category_id=self.category_id, 
                slug=self.slug
            )

class MenuItem(models.Model):
    item_id = models.CharField(max_length=255, unique=True, editable=False)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu/items/', null=True, blank=True)
    available = models.BooleanField(default=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    is_popular = models.BooleanField(default=False)
    addons = models.ManyToManyField('Addon', related_name='menu_items', blank=True)

    def save(self,*args, **kwargs):
        new = self.pk is None
        super().save(*args,**kwargs)

        if new and not self.item_id:
            self.item_id = f"menu_item_{self.pk:03d}"
            MenuItem.objects.filter(pk=self.pk).update(item_id=self.item_id)

class Addon(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)