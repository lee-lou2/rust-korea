from rest_framework import serializers
from apps.users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필 시리얼라이저"""

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "nickname",
            "introduction",
            "avatar",
        ]
