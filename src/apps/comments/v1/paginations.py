from rest_framework.pagination import CursorPagination


class CommentCursorPagination(CursorPagination):
    """댓글 페이지네이션"""

    ordering = "-likes_count", "reported_count", "-created_at"
    page_size = 10
