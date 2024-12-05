from allauth.account.views import LogoutView
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.socialaccount.providers.google.urls")),
    # logout
    path("accounts/logout/", LogoutView.as_view(), name="account_logout"),
    path("v1/", include("apps.feeds.v1.urls")),
    path("v1/", include("apps.comments.v1.urls")),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
