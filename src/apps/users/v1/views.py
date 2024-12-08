from rest_framework import viewsets, mixins, exceptions, response
from rest_framework.permissions import IsAuthenticated

from apps.users.models import UserProfile
from apps.users.v1.serializers import UserProfileSerializer


class UserProfileViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    """사용자 프로필 뷰셋"""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "user"

    def get_object(self):
        if self.kwargs.get(self.lookup_url_kwarg) != "me":
            raise exceptions.PermissionDenied("권한이 없습니다.")
        if not hasattr(self.request.user, "profile"):
            raise exceptions.PermissionDenied("프로필이 없습니다.")
        return self.request.user.profile

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class UserCountAPIView(viewsets.GenericViewSet):
    """사용자 카운트 뷰셋"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return response.Response(
            {
                "feeds": request.user.feeds.count(),
                "comments": request.user.comments.count(),
                "likes": request.user.feed_likes.count(),
            }
        )
