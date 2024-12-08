from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """사용자 프로필"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=50, unique=True, help_text="닉네임")
    introduction = models.CharField(
        max_length=255, null=True, blank=True, help_text="소개"
    )
    avatar = models.URLField(
        blank=True,
        null=True,
        help_text="프로필 이미지",
    )
    scopes = models.CharField(
        max_length=255,
        help_text="권한들",
        null=True,
        blank=True,
    )
    # 기본 설정
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profiles"
        verbose_name = "사용자 프로필"
        verbose_name_plural = "사용자 프로필들"
