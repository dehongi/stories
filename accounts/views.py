from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.http import JsonResponse
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomPasswordChangeForm,
)
from .models import CustomUser, Follow


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully! Please log in.")
        return response


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("website:home")

    def form_valid(self, form):
        response = super().form_valid(form)

        user = form.get_user()
        messages.success(
            self.request,
            f"Welcome back, {user.first_name or user.email}!",
        )
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("website:home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        messages.success(self.request, "Your password has been updated successfully.")
        return super().form_valid(form)


@login_required
def profile_view(request):
    user = request.user
    return render(request, "accounts/profile.html", {"user": user})


class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "accounts/user_detail.html"
    context_object_name = "profile_user"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()

        # Get followers and following counts
        context["followers_count"] = profile_user.follower_count()
        context["following_count"] = profile_user.following_count()

        # Check if the current user is following the profile user
        if self.request.user.is_authenticated:
            context["is_following"] = self.request.user.is_following(profile_user)

        # Get the user's stories
        context["stories"] = profile_user.stories.filter(is_published=True).order_by(
            "-created_at"
        )

        # Get the user's reading lists (public ones only if not the profile owner)
        if self.request.user == profile_user:
            context["reading_lists"] = profile_user.reading_lists.all()
        else:
            context["reading_lists"] = profile_user.reading_lists.filter(is_public=True)

        return context


@login_required
def follow_user(request, slug):
    """Follow a user."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    user_to_follow = get_object_or_404(CustomUser, slug=slug)
    current_user = request.user

    # Don't allow users to follow themselves
    if user_to_follow == current_user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("accounts:user_detail", slug=slug)

    # Create the follow relationship if it doesn't exist
    if not current_user.is_following(user_to_follow):
        Follow.objects.create(follower=current_user, followed=user_to_follow)
        messages.success(
            request, f"You are now following {user_to_follow.get_full_name()}."
        )

    # Redirect back to the user's profile
    return redirect("accounts:user_detail", slug=slug)


@login_required
def unfollow_user(request, slug):
    """Unfollow a user."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    user_to_unfollow = get_object_or_404(CustomUser, slug=slug)
    current_user = request.user

    # Delete the follow relationship if it exists
    follow_relationship = Follow.objects.filter(
        follower=current_user, followed=user_to_unfollow
    ).first()

    if follow_relationship:
        follow_relationship.delete()
        messages.success(
            request, f"You are no longer following {user_to_unfollow.get_full_name()}."
        )

    # Redirect back to the user's profile
    return redirect("accounts:user_detail", slug=slug)


@login_required
def toggle_follow(request, slug):
    """Toggle follow/unfollow a user."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    user_to_toggle = get_object_or_404(CustomUser, slug=slug)
    current_user = request.user

    # Don't allow users to follow themselves
    if user_to_toggle == current_user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("accounts:user_detail", slug=slug)

    # Check if already following
    is_following = current_user.is_following(user_to_toggle)

    if is_following:
        # Unfollow
        Follow.objects.filter(follower=current_user, followed=user_to_toggle).delete()
        messages.success(
            request, f"You are no longer following {user_to_toggle.get_full_name()}."
        )
    else:
        # Follow
        Follow.objects.create(follower=current_user, followed=user_to_toggle)
        messages.success(
            request, f"You are now following {user_to_toggle.get_full_name()}."
        )

    # Redirect back to the user's profile
    return redirect("accounts:user_detail", slug=slug)


class FollowersListView(ListView):
    model = Follow
    template_name = "accounts/followers_list.html"
    context_object_name = "followers"
    paginate_by = 20

    def get_queryset(self):
        self.user = get_object_or_404(CustomUser, slug=self.kwargs["slug"])
        return Follow.objects.filter(followed=self.user).select_related("follower")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.user
        return context


class FollowingListView(ListView):
    model = Follow
    template_name = "accounts/following_list.html"
    context_object_name = "following"
    paginate_by = 20

    def get_queryset(self):
        self.user = get_object_or_404(CustomUser, slug=self.kwargs["slug"])
        return Follow.objects.filter(follower=self.user).select_related("followed")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.user
        return context
