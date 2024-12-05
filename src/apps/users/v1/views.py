from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from apps.users.models import UserProfile
from apps.users.v1.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """사용자 프로필 뷰셋"""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
