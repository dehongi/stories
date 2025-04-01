from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify
import re


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for email-based authentication instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Allows for easy addition of custom fields in the future.
    """

    # Required fields
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Additional fields
    bio = models.TextField(blank=True, null=True)

    # Replace ImageField with ProcessedImageField for automatic processing
    profile_picture = ProcessedImageField(
        upload_to="profile_pictures/",
        processors=[ResizeToFill(500, 500)],  # Crop and resize to 500x500
        format="JPEG",  # Save as JPEG
        options={"quality": 85},  # Set JPEG quality
        blank=True,
        null=True,
    )

    email = models.EmailField(unique=True, db_index=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    username = None  # Remove username since email is used instead

    slug = models.SlugField(max_length=50, unique=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def follower_count(self):
        """Return the number of users following this user."""
        return self.followers.count()

    def following_count(self):
        """Return the number of users this user is following."""
        return self.following.count()

    def is_following(self, user):
        """Check if this user is following the given user."""
        return self.following.filter(followed=user).exists()

    def save(self, *args, **kwargs):
        if not self.slug:
            # Get the username portion of the email (before @)
            email_name = self.email.split("@")[0]

            # Remove special characters and replace with hyphens
            base_slug = re.sub(r"[^\w\s-]", "-", email_name.lower())
            base_slug = re.sub(r"[-\s]+", "-", base_slug).strip("-")

            # If user has a name, try to incorporate it into the slug
            if self.first_name and self.last_name:
                name_slug = slugify(f"{self.first_name}-{self.last_name}")
                # Use combination of name and email if possible
                if len(name_slug) > 5:  # Only use name if it creates a reasonable slug
                    base_slug = name_slug

            # Ensure uniqueness by adding a suffix if needed
            slug = base_slug
            counter = 1

            while CustomUser.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Follow(models.Model):
    """
    Model to represent following relationships between users.
    """

    follower = models.ForeignKey(
        CustomUser, related_name="following", on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        CustomUser, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "followed")

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
