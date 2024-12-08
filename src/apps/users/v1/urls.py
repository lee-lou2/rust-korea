from django.urls import path

from apps.users.v1.views import UserProfileViewSet, UserCountAPIView

urlpatterns = [
    path(
        "users/<str:user>/profile/",
        UserProfileViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "put": "update"}
        ),
    ),
    path(
        "users/me/count/",
        UserCountAPIView.as_view({"get": "get"}),
    ),
]
