from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm,
)
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for user signup with Bootstrap 5.3 styling
    """

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        )
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating existing users with Bootstrap 5.3 styling
    """

    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
    )
    profile_picture = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "bio", "profile_picture")


class CustomLoginForm(AuthenticationForm):
    """
    Form for user login with Bootstrap 5.3 styling
    """

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )


class CustomPasswordResetForm(PasswordResetForm):
    """
    Form for requesting a password reset with Bootstrap 5.3 styling
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        )
    )


class CustomSetPasswordForm(SetPasswordForm):
    """
    Form for setting a new password with Bootstrap 5.3 styling
    """

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm New Password"}
        )
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Form for changing password with Bootstrap 5.3 styling
    """

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Current Password"}
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm New Password"}
        )
    )
