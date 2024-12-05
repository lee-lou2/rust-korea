import uuid
from html import escape

from rest_framework import serializers, exceptions

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
            "likes_count",
            "comments_count",
            "reported_count",
            "is_like",
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

    def update(self, instance, validated_data):
        instance.delete()
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

    class Meta:
        model = FeedReport
        fields = [
            "feed",
            "user",
            "reason",
        ]
