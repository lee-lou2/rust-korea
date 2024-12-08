from django.contrib import admin

from .models import Feed, FeedCategory, FeedReport, FeedLike


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    """피드 관리자 페이지"""

    list_display = [
        "uuid",
        "user",
        "category",
        "content",
        "likes_count",
        "comments_count",
        "reported_count",
        "is_displayed",
        "published_at",
        "created_at",
        "updated_at",
    ]


@admin.register(FeedCategory)
class FeedCategoryAdmin(admin.ModelAdmin):
    """피드 카테고리 관리자 페이지"""

    list_display = [
        "key",
        "name",
        "emoji",
        "color",
        "scope",
        "is_displayed",
        "created_at",
        "updated_at",
    ]


@admin.register(FeedReport)
class FeedReportAdmin(admin.ModelAdmin):
    """피드 신고 관리자 페이지"""

    list_display = [
        "user",
        "feed",
        "reason",
        "created_at",
    ]


@admin.register(FeedLike)
class FeedLikeAdmin(admin.ModelAdmin):
    """피드 좋아요 관리자 페이지"""

    list_display = [
        "user",
        "feed",
        "created_at",
    ]
