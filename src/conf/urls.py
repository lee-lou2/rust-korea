from allauth.account.views import LogoutView
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import path
from django.urls.conf import include

from django.shortcuts import render

from apps.feeds.v1.views import LatestFeed, FeedSitemap


urlpatterns = [
    path(
        "",
        lambda request: render(request, "index.html"),
        name="index",
    ),
    path(
        "robots.txt",
        lambda request: HttpResponse(
            "User-agent: *\nDisallow: /admin/\nDisallow: /static/\n",
            content_type="text/plain",
        ),
    ),
    path("rss", LatestFeed(), name="latest_feed"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"feeds": FeedSitemap}},
        name="sitemap",
    ),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.socialaccount.providers.google.urls")),
    # logout
    path("accounts/logout/", LogoutView.as_view(), name="account_logout"),
    path("api/v1/", include("apps.feeds.v1.urls")),
    path("api/v1/", include("apps.comments.v1.urls")),
    path("api/v1/", include("apps.users.v1.urls")),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
