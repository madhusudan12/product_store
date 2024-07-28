from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from metadata_store.models import Product


def invalidate_caches(keys_format_list):
    """
    Invalidates cache entries matching the provided key formats.

    Args:
        keys_format_list (list): List of cache key formats to invalidate.
    """
    for key_format in keys_format_list:
        for key in cache.keys(key_format):
            cache.delete(key)


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_cache(sender, instance, **kwargs):
    """
    Clears cache entries related to the Product model after save or delete operations.

    Args:
        sender (Model): The model class that sent the signal.
        instance (Product): The instance of the Product model.
        **kwargs: Additional keyword arguments.
    """
    key_formats = [f"product_list:*", f'product_retrieve:{instance.pk}:*']
    invalidate_caches(key_formats)
