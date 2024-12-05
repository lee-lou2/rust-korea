from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import FeedCategory


@receiver([post_save, post_delete], sender=FeedCategory)
def clear_feed_category_cache(sender, **kwargs):
    """피드 카테고리 캐시 삭제 시그널"""
    cache_key = f"feed_category:list:{settings.DJANGO_ENVIRONMENT}"
    cache.delete(cache_key)
