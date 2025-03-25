from django import forms
from .models import Story, Category, Comment, UserPreference, ReadingList


class CategoryForm(forms.ModelForm):
    """
    ModelForm for creating and updating categories
    """

    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Category Name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Brief description (optional)",
                }
            ),
        }


class StoryForm(forms.ModelForm):
    """
    ModelForm for creating and updating stories
    """

    class Meta:
        model = Story
        fields = ["title", "content", "categories", "is_published"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Story Title"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 15,
                    "placeholder": "Write your story here...",
                }
            ),
            "categories": forms.SelectMultiple(attrs={"class": "form-select"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CommentForm(forms.ModelForm):
    """
    ModelForm for creating and updating comments
    """

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write your comment here...",
                }
            )
        }
        labels = {"content": "Comment"}


class UserPreferenceForm(forms.ModelForm):
    """
    ModelForm for updating user preferences
    """

    class Meta:
        model = UserPreference
        fields = ["favorite_categories"]
        widgets = {
            "favorite_categories": forms.SelectMultiple(attrs={"class": "form-select"})
        }


class ReadingListForm(forms.ModelForm):
    """
    ModelForm for creating and updating reading lists
    """

    class Meta:
        model = ReadingList
        fields = ["name", "description", "is_public", "stories"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Reading List Name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Brief description of your reading list",
                }
            ),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "stories": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
