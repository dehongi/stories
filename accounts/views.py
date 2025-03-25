from django.shortcuts import render, redirect
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
from django.views.generic import CreateView, UpdateView
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomPasswordChangeForm,
)
from .models import CustomUser


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
    success_url = reverse_lazy("profile")

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
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)
