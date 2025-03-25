from django.contrib import admin
from .models import Story, Category, Comment, UserPreference, ReadingList


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_at", "is_published"]
    list_filter = ["is_published", "created_at", "categories"]
    search_fields = ["title", "content", "author__username"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    filter_horizontal = ["categories"]
    date_hierarchy = "created_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "story", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["content", "user__username", "story__title"]
    raw_id_fields = ["user", "story"]


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user__username"]
    filter_horizontal = ["favorite_categories"]


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "user__username"]
    filter_horizontal = ["stories"]
