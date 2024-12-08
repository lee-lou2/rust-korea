import uuid
from html import escape

from django.db import transaction
from rest_framework import serializers, exceptions

from apps.comments.v1.serializers import CommentSerializer
from apps.feeds.v1.fields import CurrentFeed
from apps.feeds.models import Feed, FeedLike, FeedCategory, FeedReport
from apps.users.v1.serializers import UserProfileSerializer


class FeedCategorySerializer(serializers.ModelSerializer):
    """피드 카테고리 시리얼라이저"""

    class Meta:
        model = FeedCategory
        fields = [
            "id",
            "key",
            "name",
            "emoji",
            "color",
        ]


class FeedSerializer(serializers.ModelSerializer):
    """피드 시리얼라이저"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_profile = UserProfileSerializer(source="user.profile", read_only=True)
    category_info = FeedCategorySerializer(source="category", read_only=True)
    is_like = serializers.BooleanField(
        help_text="좋아요 여부", default=False, read_only=True
    )
    is_reported = serializers.BooleanField(
        help_text="신고 여부", default=False, read_only=True
    )
    best_comment = serializers.SerializerMethodField(
        help_text="베스트 댓글", read_only=True
    )

    def get_best_comment(self, instance):
        instance = (
            instance.comments.filter(is_displayed=True).order_by("-likes_count").first()
        )
        serializer = CommentSerializer(instance=instance) if instance else None
        return serializer.data if instance else None

    def validate_category(self, attr):
        if self.instance and self.instance.category != attr:
            raise exceptions.ValidationError("카테고리는 수정할 수 없습니다.")
        return attr

    def validate_content(self, attr):
        return escape(attr, quote=True)

    def create(self, validated_data):
        validated_data["uuid"] = uuid.uuid4()
        return super().create(validated_data)

    class Meta:
        model = Feed
        fields = [
            "uuid",
            "user",
            "user_profile",
            "category",
            "category_info",
            "content",
            "link",
            "best_comment",
            "likes_count",
            "comments_count",
            "reported_count",
            "is_like",
            "is_reported",
            "is_displayed",
            "published_at",
        ]
        read_only_fields = [
            "uuid",
            "likes_count",
            "comments_count",
            "reported_count",
            "is_displayed",
        ]


class FeedLikeSerializer(serializers.ModelSerializer):
    """피드 좋아요 시리얼라이저"""

    feed = serializers.HiddenField(default=CurrentFeed())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_like = serializers.BooleanField(
        help_text="좋아요 여부", default=True, read_only=True
    )

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        self.instance = FeedLike.objects.filter(
            feed=data.get("feed"), user=data.get("user")
        ).first()
        return data

    @transaction.atomic
    def create(self, validated_data):
        # 피드 좋아요
        instance = super().create(validated_data)
        # 피드 좋아요 수 증가
        instance.feed.likes_count += 1
        instance.feed.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        # 피드 좋아요 취소
        instance.delete()
        # 피드 좋아요 수 감소
        feed = validated_data.get("feed")
        feed.likes_count -= 1 if feed.likes_count > 0 else 0
        feed.save()
        return {"is_like": False}

    class Meta:
        model = FeedLike
        fields = [
            "feed",
            "user",
            "is_like",
        ]


class FeedReportSerializer(serializers.ModelSerializer):
    """피드 신고 시리얼라이저"""

    feed = serializers.HiddenField(default=CurrentFeed())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        # 신고 수 증가
        instance.feed.reported_count += 1
        instance.feed.save()
        return instance

    class Meta:
        model = FeedReport
        fields = [
            "feed",
            "user",
            "reason",
        ]
