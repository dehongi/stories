from django.urls import path
from . import views

app_name = "stories"

urlpatterns = [
    # Story URLs
    path("", views.StoryListView.as_view(), name="story_list"),
    path(
        "category/<slug:category_slug>/",
        views.StoryListView.as_view(),
        name="story_list_by_category",
    ),
    path("story/new/", views.StoryCreateView.as_view(), name="story_create"),
    path("story/<slug:slug>/", views.StoryDetailView.as_view(), name="story_detail"),
    path(
        "story/<slug:slug>/edit/", views.StoryUpdateView.as_view(), name="story_update"
    ),
    path(
        "story/<slug:slug>/delete/",
        views.StoryDeleteView.as_view(),
        name="story_delete",
    ),
    path("my-stories/", views.UserStoryListView.as_view(), name="my_stories"),
    # Category URLs
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("category/new/", views.CategoryCreateView.as_view(), name="category_create"),
    path(
        "category/<slug:slug>/edit/",
        views.CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "category/<slug:slug>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    # Comment URLs
    path("story/<slug:slug>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    # Reading List URLs
    path(
        "reading-lists/", views.ReadingListListView.as_view(), name="reading_list_list"
    ),
    path(
        "reading-list/<int:pk>/",
        views.ReadingListDetailView.as_view(),
        name="reading_list_detail",
    ),
    path(
        "reading-list/new/",
        views.ReadingListCreateView.as_view(),
        name="reading_list_create",
    ),
    path(
        "reading-list/<int:pk>/edit/",
        views.ReadingListUpdateView.as_view(),
        name="reading_list_update",
    ),
    path(
        "reading-list/<int:pk>/delete/",
        views.ReadingListDeleteView.as_view(),
        name="reading_list_delete",
    ),
    path(
        "story/<slug:slug>/add-to-reading-list/",
        views.add_to_reading_list,
        name="add_to_reading_list",
    ),
    path(
        "story/<slug:slug>/remove-from-reading-list/<int:reading_list_id>/",
        views.remove_from_reading_list,
        name="remove_from_reading_list",
    ),
    # User Preference URLs
    path(
        "preferences/",
        views.UserPreferenceUpdateView.as_view(),
        name="user_preferences",
    ),
]
