from django.urls import path
from rest_framework import routers

from .views import (
    FeedViewSet,
    FeedCategoryViewSet,
    FeedLikeViewSet,
    FeedReportViewSet,
)

router = routers.SimpleRouter()
router.register("feeds/categories", FeedCategoryViewSet)
router.register("feeds", FeedViewSet)


urlpatterns = router.urls + [
    path(
        "feeds/<str:feed_uuid>/like/",
        FeedLikeViewSet.as_view({"post": "create"}),
        name="feed-like",
    ),
    path(
        "feeds/<str:feed_uuid>/report/",
        FeedReportViewSet.as_view({"post": "create"}),
        name="feed-report",
    ),
]
