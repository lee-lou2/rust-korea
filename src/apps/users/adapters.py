import random
import string

from .models import UserProfile

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # 기본 설정
        extra_data = sociallogin.account.extra_data
        # 4자리 랜덤 값
        random_keys = random.choices(string.ascii_letters + string.digits, k=4)
        google_name = extra_data.get("name", "") + "_" + "".join(random_keys)
        google_avatar = extra_data.get("picture", "")
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "nickname": google_name,
                "avatar": google_avatar,
            },
        )
        return user
