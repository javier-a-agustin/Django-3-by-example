from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "author",
        "publish",
        "status",
    )
    list_filter = (
        "status",
        "created",
        "publish",
        "author",
    )
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "post_id",
        "created",
        "active",
    )
    list_filter = ("active", "created", "updated")
    search_fields = ("name", "email", "body")
    ordering = ("-post_id__title",)
