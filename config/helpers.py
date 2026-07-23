from django.utils.text import slugify

def generate_unique_slug(instance, base_text, slug_field='slug'):
    """Appends -2, -3, etc. if the base slug is already taken by another row."""
    base_slug = slugify(base_text)
    slug = base_slug
    ModelClass = instance.__class__
    counter = 2
    while ModelClass.objects.filter(**{slug_field: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug