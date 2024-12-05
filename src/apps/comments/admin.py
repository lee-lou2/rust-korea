from django.contrib import admin

from .models import Comment, CommentReport, CommentLike


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """댓글 관리자 페이지"""

    list_display = [
        "id",
        "parent",
        "user",
        "feed",
        "content",
        "likes_count",
        "reported_count",
        "reply_count",
        "is_displayed",
        "created_at",
        "updated_at",
    ]


@admin.register(CommentReport)
class CommentReportAdmin(admin.ModelAdmin):
    """댓글 신고 관리자 페이지"""

    list_display = [
        "id",
        "user",
        "comment",
        "reason",
        "created_at",
    ]


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    """댓글 좋아요 관리자 페이지"""

    list_display = [
        "id",
        "user",
        "comment",
        "created_at",
    ]
