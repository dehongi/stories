from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from django.db.models import Q
from .models import Story, Category, Comment, UserPreference, ReadingList
from .forms import (
    StoryForm,
    CategoryForm,
    CommentForm,
    UserPreferenceForm,
    ReadingListForm,
)


class StoryListView(ListView):
    model = Story
    template_name = "stories/story_list.html"
    context_object_name = "stories"
    paginate_by = 9

    def get_queryset(self):
        queryset = Story.objects.filter(is_published=True).order_by("-created_at")

        # Filter by category if specified in URL
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(categories=category)

        # Search functionality
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(author__first_name__icontains=query)
                | Q(author__last_name__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        # Add category to context if filtering by category
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            context["current_category"] = get_object_or_404(
                Category, slug=category_slug
            )

        # Add search query to context
        context["search_query"] = self.request.GET.get("q", "")

        return context


class StoryDetailView(DetailView):
    model = Story
    template_name = "stories/story_detail.html"
    context_object_name = "story"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()

        # If user is not the author, only show published stories
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return queryset
        elif self.request.user.is_authenticated:
            return queryset.filter(Q(is_published=True) | Q(author=self.request.user))
        else:
            return queryset.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(is_approved=True).order_by(
            "-created_at"
        )
        context["comment_form"] = CommentForm()

        # Check if story is in user's reading list
        if self.request.user.is_authenticated:
            try:
                user_reading_lists = self.request.user.reading_lists.all()
                context["user_reading_lists"] = user_reading_lists
                context["in_reading_lists"] = user_reading_lists.filter(
                    stories=self.object
                ).exists()
            except:
                pass

        return context


class StoryCreateView(LoginRequiredMixin, CreateView):
    model = Story
    form_class = StoryForm
    template_name = "stories/story_form.html"
    success_url = reverse_lazy("stories:my_stories")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your story has been created successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create New Story"
        context["submit_text"] = "Create Story"
        return context


class StoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Story
    form_class = StoryForm
    template_name = "stories/story_form.html"

    def get_success_url(self):
        return reverse_lazy("stories:story_detail", kwargs={"slug": self.object.slug})

    def test_func(self):
        story = self.get_object()
        return self.request.user == story.author or self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Your story has been updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Story"
        context["submit_text"] = "Update Story"
        return context


class StoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Story
    template_name = "stories/story_confirm_delete.html"
    success_url = reverse_lazy("stories:my_stories")
    context_object_name = "story"

    def test_func(self):
        story = self.get_object()
        return self.request.user == story.author or self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your story has been deleted successfully!")
        return super().delete(request, *args, **kwargs)


class UserStoryListView(LoginRequiredMixin, ListView):
    model = Story
    template_name = "stories/user_stories.html"
    context_object_name = "stories"
    paginate_by = 10

    def get_queryset(self):
        return Story.objects.filter(author=self.request.user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["published_count"] = (
            self.get_queryset().filter(is_published=True).count()
        )
        context["draft_count"] = self.get_queryset().filter(is_published=False).count()
        return context


class CategoryListView(ListView):
    model = Category
    template_name = "stories/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "stories/category_detail.html"
    context_object_name = "category"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stories"] = self.object.stories.filter(is_published=True).order_by(
            "-created_at"
        )
        return context


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "stories/category_form.html"
    success_url = reverse_lazy("stories:category_list")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Category has been created successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create New Category"
        context["submit_text"] = "Create Category"
        return context


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "stories/category_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "stories:category_detail", kwargs={"slug": self.object.slug}
        )

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Category has been updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Category"
        context["submit_text"] = "Update Category"
        return context


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = "stories/category_confirm_delete.html"
    success_url = reverse_lazy("stories:category_list")
    context_object_name = "category"

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Category has been deleted successfully!")
        return super().delete(request, *args, **kwargs)


# Comment views
def add_comment(request, slug):
    story = get_object_or_404(Story, slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment has been added successfully!")
            return redirect("stories:story_detail", slug=slug)

    return redirect("stories:story_detail", slug=slug)


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    story_slug = comment.story.slug

    # Check if user is the comment author or staff
    if request.user == comment.user or request.user.is_staff:
        comment.delete()
        messages.success(request, "Comment has been deleted successfully!")
    else:
        messages.error(request, "You are not authorized to delete this comment.")

    return redirect("stories:story_detail", slug=story_slug)


# Reading List Views
class ReadingListListView(LoginRequiredMixin, ListView):
    model = ReadingList
    template_name = "stories/reading_list_list.html"
    context_object_name = "reading_lists"

    def get_queryset(self):
        return self.request.user.reading_lists.all().order_by("-created_at")


class ReadingListDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ReadingList
    template_name = "stories/reading_list_detail.html"
    context_object_name = "reading_list"

    def test_func(self):
        reading_list = self.get_object()
        return self.request.user == reading_list.user


class ReadingListCreateView(LoginRequiredMixin, CreateView):
    model = ReadingList
    form_class = ReadingListForm
    template_name = "stories/reading_list_form.html"
    success_url = reverse_lazy("stories:story_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Reading list has been created successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create New Reading List"
        context["submit_text"] = "Create Reading List"
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show published stories in the form
        form.fields["stories"].queryset = Story.objects.filter(is_published=True)
        return form


class ReadingListUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReadingList
    form_class = ReadingListForm
    template_name = "stories/reading_list_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "stories:reading_list_detail", kwargs={"pk": self.object.pk}
        )

    def test_func(self):
        reading_list = self.get_object()
        return self.request.user == reading_list.user

    def form_valid(self, form):
        messages.success(self.request, "Reading list has been updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Reading List"
        context["submit_text"] = "Update Reading List"
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show published stories in the form
        form.fields["stories"].queryset = Story.objects.filter(is_published=True)
        return form


class ReadingListDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReadingList
    template_name = "stories/reading_list_confirm_delete.html"
    success_url = reverse_lazy("stories:story_list")
    context_object_name = "reading_list"

    def test_func(self):
        reading_list = self.get_object()
        return self.request.user == reading_list.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Reading list has been deleted successfully!")
        return super().delete(request, *args, **kwargs)


def add_to_reading_list(request, slug):
    if request.method == "POST":
        story = get_object_or_404(Story, slug=slug)
        reading_list_id = request.POST.get("reading_list")

        if reading_list_id:
            reading_list = get_object_or_404(
                ReadingList, id=reading_list_id, user=request.user
            )
            reading_list.stories.add(story)
            messages.success(
                request, f'Story added to "{reading_list.name}" reading list!'
            )

    return redirect("stories:story_detail", slug=slug)


def remove_from_reading_list(request, slug, reading_list_id):
    story = get_object_or_404(Story, slug=slug)
    reading_list = get_object_or_404(ReadingList, id=reading_list_id, user=request.user)

    reading_list.stories.remove(story)
    messages.success(request, f'Story removed from "{reading_list.name}" reading list!')

    # Redirect back to the reading list or the story
    referer = request.META.get("HTTP_REFERER")
    if referer and "reading-list" in referer:
        return redirect("stories:reading_list_detail", pk=reading_list_id)

    return redirect("stories:story_detail", slug=slug)


# User Preference View
class UserPreferenceUpdateView(LoginRequiredMixin, UpdateView):
    model = UserPreference
    form_class = UserPreferenceForm
    template_name = "stories/user_preference_form.html"
    success_url = reverse_lazy("stories:story_list")

    def get_object(self, queryset=None):
        # Get the user's preferences or create if it doesn't exist
        obj, created = UserPreference.objects.get_or_create(
            user=self.request.user,
        )
        return obj

    def form_valid(self, form):
        messages.success(
            self.request, "Your preferences have been updated successfully!"
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Reading Preferences"
        context["submit_text"] = "Save Preferences"
        return context
