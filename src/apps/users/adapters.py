from .models import UserProfile

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # 기본 설정
        extra_data = sociallogin.account.extra_data
        google_name = extra_data.get("name", "")
        google_avatar = extra_data.get("picture", "")
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "nickname": google_name,
                "avatar": google_avatar,
            },
        )
        return user
