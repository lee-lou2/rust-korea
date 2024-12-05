from django.contrib.auth.models import User
from django.db import models


class FeedCategory(models.Model):
    """피드 카테고리"""

    key = models.CharField(max_length=50, unique=True, help_text="키")
    name = models.CharField(max_length=50, help_text="이름")
    emoji = models.CharField(max_length=1, help_text="이모지")
    color = models.CharField(max_length=255, help_text="색상")
    scope = models.CharField(max_length=50, help_text="권한", null=True, blank=True)
    # 기본 설정
    is_displayed = models.BooleanField(default=True, help_text="표시 여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feed_categories"
        verbose_name = "피드 카테고리"
        verbose_name_plural = "피드 카테고리들"


class Feed(models.Model):
    """피드"""

    uuid = models.UUIDField(primary_key=True, help_text="UUID")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feeds",
        help_text="사용자",
    )
    category = models.ForeignKey(
        FeedCategory,
        on_delete=models.CASCADE,
        related_name="feeds",
        help_text="카테고리",
    )
    content = models.CharField(max_length=1000, help_text="내용")
    # 카운트
    likes_count = models.IntegerField(default=0, help_text="좋아요 수")
    comments_count = models.IntegerField(default=0, help_text="댓글 수")
    reported_count = models.IntegerField(default=0, help_text="신고 횟수")
    # 기본 설정
    is_displayed = models.BooleanField(default=True, help_text="표시 여부")
    published_at = models.DateTimeField(help_text="게시 일시")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "feeds"
        verbose_name = "피드"
        verbose_name_plural = "피드들"


class FeedReport(models.Model):
    """피드 신고하기"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feed_reports",
        help_text="사용자",
    )
    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        related_name="reports",
        help_text="피드",
    )
    reason = models.TextField(help_text="사유")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "feed_reports"
        verbose_name = "피드 신고"
        verbose_name_plural = "피드 신고들"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "feed"], name="unique_user_feed_report"
            )
        ]


class FeedLike(models.Model):
    """피드 좋아요"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feed_likes",
        help_text="사용자",
    )
    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        related_name="likes",
        help_text="피드",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "feed_likes"
        verbose_name = "피드 좋아요"
        verbose_name_plural = "피드 좋아요들"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "feed"], name="unique_user_feed_like"
            )
        ]
