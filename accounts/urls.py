from django.urls import path
from .views import (
    SignUpView,
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    CustomPasswordChangeView,
    profile_view,
    ProfileUpdateView,
    UserDetailView,
    follow_user,
    unfollow_user,
    toggle_follow,
    FollowersListView,
    FollowingListView,
)

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "password-change/", CustomPasswordChangeView.as_view(), name="password_change"
    ),
    path("profile/", profile_view, name="profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update"),
    # User detail and follow system
    path("user/<slug:slug>/", UserDetailView.as_view(), name="user_detail"),
    path("user/<slug:slug>/follow/", follow_user, name="follow_user"),
    path("user/<slug:slug>/unfollow/", unfollow_user, name="unfollow_user"),
    path("user/<slug:slug>/toggle-follow/", toggle_follow, name="toggle_follow"),
    path(
        "user/<slug:slug>/followers/",
        FollowersListView.as_view(),
        name="followers_list",
    ),
    path(
        "user/<slug:slug>/following/",
        FollowingListView.as_view(),
        name="following_list",
    ),
]
