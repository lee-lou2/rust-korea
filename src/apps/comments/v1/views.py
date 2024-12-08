from django.db import transaction
from django.db.models import Exists, OuterRef
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from apps.comments.models import Comment, CommentLike, CommentReport
from apps.comments.v1.paginations import CommentCursorPagination
from apps.comments.v1.serializers import (
    CommentSerializer,
    CommentLikeSerializer,
    CommentReportSerializer,
    CommentListSerializer,
)
from apps.feeds.models import Feed


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    """댓글 뷰셋"""

    queryset = Comment.objects.filter(is_displayed=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_scope = "comment:create"
    pagination_class = CommentCursorPagination

    def get_current_feed(self):
        return Feed.objects.get(uuid=self.kwargs["feed_uuid"])

    def get_throttles(self):
        if self.action == "create":
            return [ScopedRateThrottle()]
        return super().get_throttles()

    def get_queryset(self):
        feed_uuid = self.kwargs.get("feed_uuid")
        queryset = super().get_queryset().filter(feed__uuid=feed_uuid)
        if self.action == "list":
            queryset = (
                queryset.select_related("user__profile")
                .prefetch_related("replies")
                .filter(parent=None)
            )
        elif self.action in ["update", "partial_update", "destroy"]:
            # 직접 작성한 피드만 수정, 삭제 가능
            queryset = queryset.filter(user=self.request.user)
        if self.action in "list" and self.request.user.is_authenticated:
            # 로그인 사용자의 경우 좋아요 여부
            queryset = queryset.prefetch_related("likes").annotate(
                is_like=Exists(
                    CommentLike.objects.filter(
                        comment=OuterRef("pk"), user=self.request.user
                    )
                ),
                is_reported=Exists(
                    CommentReport.objects.filter(
                        comment=OuterRef("pk"), user=self.request.user
                    )
                ),
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        return CommentSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @transaction.atomic
    def perform_destroy(self, instance):
        # 피드의 댓글 수 감소
        if instance.parent is None:
            instance.feed.comments_count -= 1 if instance.feed.comments_count > 0 else 0
            instance.feed.save()
        # 부모 댓글의 답글 수 감소
        if instance.parent:
            instance.parent.reply_count -= 1 if instance.parent.reply_count > 0 else 0
            instance.parent.save()
        return super().perform_destroy(instance)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CommentLikeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """댓글 좋아요 뷰셋"""

    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = "comment_like:all"
    throttle_classes = [ScopedRateThrottle]

    def get_current_comment(self):
        return Comment.objects.get(pk=self.kwargs["comment_id"])

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CommentReportViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """댓글 신고 뷰셋"""

    queryset = CommentReport.objects.all()
    serializer_class = CommentReportSerializer
    permission_classes = [IsAuthenticated]

    def get_current_comment(self):
        return Comment.objects.get(pk=self.kwargs["comment_id"])

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
