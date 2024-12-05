from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """프로필 관리자 페이지"""

    list_display = [
        "user",
        "nickname",
        "introduction",
        "avatar",
        "scopes",
        "created_at",
        "updated_at",
    ]
