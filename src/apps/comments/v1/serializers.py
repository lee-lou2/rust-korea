from html import escape

from rest_framework import serializers

from apps.comments.models import Comment, CommentLike, CommentReport
from apps.comments.v1.fields import CurrentComment
from apps.users.v1.serializers import UserProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    """댓글 시리얼라이저"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_profile = UserProfileSerializer(source="user.profile", read_only=True)
    is_like = serializers.BooleanField(
        help_text="좋아요 여부", default=False, read_only=True
    )

    def validate_content(self, attr):
        return escape(attr, quote=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "parent",
            "user",
            "user_profile",
            "feed",
            "content",
            "likes_count",
            "reply_count",
            "reported_count",
            "is_like",
            "is_displayed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "likes_count",
            "reply_count",
            "reported_count",
            "is_like",
            "is_displayed",
            "created_at",
            "updated_at",
        ]


class CommentLikeSerializer(serializers.ModelSerializer):
    """댓글 좋아요 시리얼라이저"""

    comment = serializers.HiddenField(default=CurrentComment())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_like = serializers.BooleanField(
        help_text="좋아요 여부", default=True, read_only=True
    )

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        self.instance = CommentLike.objects.filter(
            comment=data.get("comment"), user=data.get("user")
        ).first()
        return data

    def update(self, instance, validated_data):
        instance.delete()
        return {"is_like": False}

    class Meta:
        model = CommentLike
        fields = [
            "comment",
            "user",
            "is_like",
        ]


class CommentReportSerializer(serializers.ModelSerializer):
    """댓글 신고 시리얼라이저"""

    comment = serializers.HiddenField(default=CurrentComment())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CommentReport
        fields = [
            "comment",
            "user",
            "reason",
        ]
