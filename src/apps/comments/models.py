from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    """댓글"""

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        help_text="부모 댓글",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="사용자",
    )
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="피드",
    )
    content = models.CharField(max_length=500, help_text="내용")
    # 카운트
    likes_count = models.IntegerField(default=0, help_text="좋아요 수")
    reported_count = models.IntegerField(default=0, help_text="신고 횟수")
    reply_count = models.IntegerField(default=0, help_text="답글 수")
    # 기본 설정
    is_displayed = models.BooleanField(default=True, help_text="표시 여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"
        verbose_name = "댓글"
        verbose_name_plural = "댓글들"


class CommentReport(models.Model):
    """댓글 신고하기"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_reports",
        help_text="사용자",
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="reports",
        help_text="댓글",
    )
    reason = models.TextField(help_text="사유")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment_reports"
        verbose_name = "댓글 신고"
        verbose_name_plural = "댓글 신고들"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"], name="unique_user_comment_report"
            )
        ]


class CommentLike(models.Model):
    """댓글 좋아요"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_likes",
        help_text="사용자",
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="likes",
        help_text="댓글",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment_likes"
        verbose_name = "댓글 좋아요"
        verbose_name_plural = "댓글 좋아요들"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"], name="unique_user_comment_like"
            )
        ]
