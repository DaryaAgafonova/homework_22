from django.core.cache import cache
from django.conf import settings
from .models import Product, Category

def get_products_by_category(category_slug):
    cache_key = f'category_products_{category_slug}'
    products = cache.get(cache_key)
    
    if products is None:
        try:
            category = Category.objects.get(slug=category_slug)
            products = list(Product.objects.filter(category=category))
            
            cache.set(cache_key, products, settings.CACHE_TTL)
        except Category.DoesNotExist:
            products = []
    
    return products