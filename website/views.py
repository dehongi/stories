from django.shortcuts import render
from stories.models import Story, Category
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()


def home_view(request):
    """
    Home page view that displays featured stories, categories, and popular authors
    """
    featured_stories = Story.objects.filter(is_published=True).order_by("-created_at")[
        :6
    ]
    categories = Category.objects.all()[:8]

    # Get popular authors based on number of published stories
    popular_authors = (
        User.objects.annotate(
            story_count=Count(
                "stories", filter=Story.objects.filter(is_published=True).values("id")
            )
        )
        .filter(story_count__gt=0)
        .order_by("-story_count")[:6]
    )

    context = {
        "featured_stories": featured_stories,
        "categories": categories,
        "popular_authors": popular_authors,
    }

    return render(request, "home.html", context)


def about_view(request):
    """
    About page view
    """
    return render(request, "website/about.html")


def contact_view(request):
    """
    Contact page view
    """
    return render(request, "website/contact.html")


def faq_view(request):
    """
    FAQ page view
    """
    return render(request, "website/faq.html")


def terms_view(request):
    """
    Terms page view
    """
    return render(request, "website/terms.html")


def privacy_view(request):
    """
    Privacy page view
    """
    return render(request, "website/privacy.html")
