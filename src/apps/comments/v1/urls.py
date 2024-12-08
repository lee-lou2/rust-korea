from django.urls import path

from .views import CommentViewSet, CommentReportViewSet, CommentLikeViewSet

urlpatterns = [
    path(
        "feeds/<str:feed_uuid>/comments/",
        CommentViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="comment",
    ),
    path(
        "feeds/<str:feed_uuid>/comments/<str:pk>/",
        CommentViewSet.as_view(
            {
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="comment",
    ),
    path(
        "feeds/<str:feed_uuid>/comments/<str:comment_id>/like/",
        CommentLikeViewSet.as_view({"post": "create"}),
        name="comment-like",
    ),
    path(
        "feeds/<str:feed_uuid>/comments/<str:comment_id>/report/",
        CommentReportViewSet.as_view({"post": "create"}),
        name="comment-report",
    ),
]
