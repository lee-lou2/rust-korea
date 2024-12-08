from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.contrib.syndication.views import Feed as FeedView
from django.core.cache import cache
from django.db.models import Exists, OuterRef
from rest_framework import viewsets, mixins, response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated,
)
from rest_framework.throttling import ScopedRateThrottle

from apps.feeds.models import Feed, FeedLike, FeedCategory, FeedReport
from apps.feeds.v1.filters import FeedFilter
from apps.feeds.v1.paginations import FeedCursorPagination
from apps.feeds.v1.serializers import (
    FeedSerializer,
    FeedLikeSerializer,
    FeedCategorySerializer,
    FeedReportSerializer,
)


class FeedCategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """피드 카테고리 뷰셋"""

    queryset = FeedCategory.objects.filter(is_displayed=True)
    serializer_class = FeedCategorySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        cache_key = f"feed_category:list:{settings.DJANGO_ENVIRONMENT}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return response.Response(cached_data)
        resp = super().list(request, *args, **kwargs)
        cache.set(cache_key, resp.data, timeout=60 * 60)
        return resp


class FeedViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    """피드 뷰셋"""

    queryset = Feed.objects.filter(is_displayed=True)
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = FeedFilter
    throttle_scope = "feed:create"
    pagination_class = FeedCursorPagination

    def get_throttles(self):
        if self.action == "create":
            return [ScopedRateThrottle()]
        return super().get_throttles()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.select_related("user__profile", "category").filter(
                category__is_displayed=True
            )
        elif self.action in ["update", "partial_update", "destroy"]:
            # 직접 작성한 피드만 수정, 삭제 가능
            queryset = queryset.filter(user=self.request.user)
        if self.action in ["list", "retrieve"] and self.request.user.is_authenticated:
            # 로그인 사용자의 경우 좋아요 여부
            queryset = queryset.prefetch_related("likes", "reports").annotate(
                is_like=Exists(
                    FeedLike.objects.filter(feed=OuterRef("pk"), user=self.request.user)
                ),
                is_reported=Exists(
                    FeedReport.objects.filter(
                        feed=OuterRef("pk"), user=self.request.user
                    )
                ),
            )
        return queryset

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class FeedLikeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """피드 좋아요 뷰셋"""

    queryset = FeedLike.objects.all()
    serializer_class = FeedLikeSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = "feed_like:all"
    throttle_classes = [ScopedRateThrottle]

    def get_current_feed(self):
        return Feed.objects.get(uuid=self.kwargs["feed_uuid"])

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class FeedReportViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """피드 신고 뷰셋"""

    queryset = FeedReport.objects.all()
    serializer_class = FeedReportSerializer
    permission_classes = [IsAuthenticated]

    def get_current_feed(self):
        return Feed.objects.get(uuid=self.kwargs["feed_uuid"])

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class LatestFeed(FeedView):
    """피드 RSS 피드"""

    title = "최신 피드"
    link = "/feeds/"
    description = "Rust Korea 의 최신 피드"

    def items(self):
        return Feed.objects.filter(is_displayed=True).order_by("-published_at")[:10]

    def item_title(self, item):
        return item.content[:50]

    def item_description(self, item):
        return item.content[:100]

    def item_link(self, item):
        return item.get_absolute_url()


class FeedSitemap(Sitemap):
    """피드 사이트맵"""

    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Feed.objects.filter(is_displayed=True)

    def lastmod(self, obj):
        return obj.updated_at
