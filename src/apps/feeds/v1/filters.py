from django_filters import rest_framework as filters
from django_filters.filters import BaseInFilter, NumberFilter
from apps.feeds.models import Feed


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class FeedFilter(filters.FilterSet):
    categories = NumberInFilter(field_name="category", lookup_expr="in")
    writer = filters.CharFilter(method="filter_writer")
    id = filters.CharFilter(field_name="uuid")

    def filter_writer(self, queryset, name, value):
        if value == "me" and self.request.user.is_authenticated:
            return queryset.filter(user=self.request.user)
        return queryset

    class Meta:
        model = Feed
        fields = {
            "published_at": ["gte", "lte"],
        }
