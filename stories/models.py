from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    """
    Categories for organizing stories by genre/theme
    """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Story(models.Model):
    """
    Main model for short stories
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stories"
    )
    content = models.TextField()
    categories = models.ManyToManyField(Category, related_name="stories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Stories"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("story_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Comments on stories
    """

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.story.title}"


class UserPreference(models.Model):
    """
    User's favorite categories and reading preferences
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences"
    )
    favorite_categories = models.ManyToManyField(
        Category, related_name="user_preferences", blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s preferences"


class ReadingList(models.Model):
    """
    Users can save stories to their reading list
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reading_lists"
    )
    stories = models.ManyToManyField(Story, related_name="in_reading_lists")
    name = models.CharField(max_length=100, default="My Reading List")
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "name"]

    def __str__(self):
        return f"{self.user.username}'s {self.name}"
