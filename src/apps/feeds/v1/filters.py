from django_filters import rest_framework as filters

from apps.feeds.models import Feed


class FeedFilter(filters.FilterSet):
    class Meta:
        model = Feed
        fields = {
            "published_at": ["gte", "lte"],
            "category": ["exact"],
        }
