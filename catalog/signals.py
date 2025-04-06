from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, Category

@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):

    cache.delete(f'product_{instance.pk}')
    
    if instance.category:
        cache.delete(f'category_products_{instance.category.slug}')

@receiver([post_save, post_delete], sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):

    cache.delete(f'category_products_{instance.slug}')