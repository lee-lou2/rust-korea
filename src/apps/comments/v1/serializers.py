from html import escape

from django.db import transaction
from django.db.models import Exists, OuterRef
from rest_framework import serializers, exceptions

from apps.comments.models import Comment, CommentLike, CommentReport
from apps.comments.v1.fields import CurrentComment
from apps.feeds.v1.fields import CurrentFeed
from apps.users.v1.serializers import UserProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    """댓글 시리얼라이저"""

    feed_content = serializers.CharField(
        source="feed.content", read_only=True, help_text="피드 내용"
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    feed = serializers.HiddenField(default=CurrentFeed())
    user_profile = UserProfileSerializer(source="user.profile", read_only=True)
    is_like = serializers.BooleanField(
        help_text="좋아요 여부", default=False, read_only=True
    )
    is_reported = serializers.BooleanField(
        help_text="신고 여부", default=False, read_only=True
    )

    def validate_content(self, attr):
        return escape(attr, quote=True)

    def validate_feed(self, attr):
        if attr and self.instance and self.instance.feed != attr:
            raise exceptions.ValidationError("피드는 수정할 수 없습니다.")
        return attr

    def validate_parent(self, attr):
        if attr and self.instance and self.instance.parent != attr:
            raise exceptions.ValidationError("부모 댓글은 수정할 수 없습니다.")
        return attr

    @transaction.atomic
    def create(self, validated_data):
        # 댓글 생성
        instance = super().create(validated_data)
        # 댓글 수 증가
        if instance.parent is None:
            instance.feed.comments_count = instance.feed.comments_count + 1
            instance.feed.save()
        # 부모 댓글의 답글 수 증가
        if instance.parent:
            instance.parent.reply_count = instance.parent.reply_count + 1
            instance.parent.save()
        return instance

    class Meta:
        model = Comment
        fields = [
            "id",
            "parent",
            "user",
            "user_profile",
            "feed",
            "feed_content",
            "content",
            "likes_count",
            "reply_count",
            "reported_count",
            "is_like",
            "is_reported",
            "is_displayed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "feed_content",
            "likes_count",
            "reply_count",
            "reported_count",
            "is_displayed",
            "created_at",
            "updated_at",
        ]


class CommentListSerializer(CommentSerializer):
    """댓글 리스트 시리얼라이저"""

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if self.context.get("request").user.is_authenticated:
            annotated_replies = instance.replies.all().annotate(
                is_like=Exists(
                    CommentLike.objects.filter(
                        comment=OuterRef("pk"), user=self.context["request"].user
                    )
                )
            )
        else:
            annotated_replies = instance.replies.all()
        ret["replies"] = CommentSerializer(
            annotated_replies, many=True, context=self.context
        ).data
        return ret


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

    @transaction.atomic
    def create(self, validated_data):
        # 댓글 좋아요
        instance = super().create(validated_data)
        # 좋아요 수 증가
        instance.comment.likes_count = instance.comment.likes_count + 1
        instance.comment.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        # 댓글 좋아요 취소
        instance.delete()
        # 좋아요 수 감소
        comment = validated_data.get("comment")
        comment.likes_count = comment.likes_count - 1 if comment.likes_count > 0 else 0
        comment.save()
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

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        # 신고 수 증가
        instance.comment.reported_count += 1
        instance.comment.save()
        return instance

    class Meta:
        model = CommentReport
        fields = [
            "comment",
            "user",
            "reason",
        ]
