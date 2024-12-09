# Generated by Django 5.1.3 on 2024-12-08 02:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.CharField(help_text="키", max_length=50, unique=True)),
                ("name", models.CharField(help_text="이름", max_length=50)),
                ("emoji", models.CharField(help_text="이모지", max_length=2)),
                ("color", models.CharField(help_text="색상", max_length=255)),
                (
                    "scope",
                    models.CharField(
                        blank=True, help_text="권한", max_length=50, null=True
                    ),
                ),
                (
                    "is_displayed",
                    models.BooleanField(default=True, help_text="표시 여부"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "피드 카테고리",
                "verbose_name_plural": "피드 카테고리들",
                "db_table": "feed_categories",
            },
        ),
        migrations.CreateModel(
            name="Feed",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        help_text="UUID", primary_key=True, serialize=False
                    ),
                ),
                ("content", models.CharField(help_text="내용", max_length=1000)),
                ("link", models.JSONField(blank=True, help_text="링크", null=True)),
                ("likes_count", models.IntegerField(default=0, help_text="좋아요 수")),
                ("comments_count", models.IntegerField(default=0, help_text="댓글 수")),
                (
                    "reported_count",
                    models.IntegerField(default=0, help_text="신고 횟수"),
                ),
                (
                    "is_displayed",
                    models.BooleanField(default=True, help_text="표시 여부"),
                ),
                ("published_at", models.DateTimeField(help_text="게시 일시")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        help_text="사용자",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feeds",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="카테고리",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feeds",
                        to="feeds.feedcategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "피드",
                "verbose_name_plural": "피드들",
                "db_table": "feeds",
            },
        ),
        migrations.CreateModel(
            name="FeedLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "feed",
                    models.ForeignKey(
                        help_text="피드",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="feeds.feed",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="사용자",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feed_likes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "피드 좋아요",
                "verbose_name_plural": "피드 좋아요들",
                "db_table": "feed_likes",
                "constraints": [
                    models.UniqueConstraint(
                        fields=("user", "feed"), name="unique_user_feed_like"
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="FeedReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reason", models.TextField(help_text="사유")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "feed",
                    models.ForeignKey(
                        help_text="피드",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reports",
                        to="feeds.feed",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="사용자",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feed_reports",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "피드 신고",
                "verbose_name_plural": "피드 신고들",
                "db_table": "feed_reports",
                "constraints": [
                    models.UniqueConstraint(
                        fields=("user", "feed"), name="unique_user_feed_report"
                    )
                ],
            },
        ),
    ]