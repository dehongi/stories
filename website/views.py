from django.shortcuts import render
from stories.models import Story, Category


def home_view(request):
    """
    Home page view that displays featured stories and categories
    """
    featured_stories = Story.objects.filter(is_published=True).order_by("-created_at")[
        :6
    ]
    categories = Category.objects.all()[:8]

    context = {
        "featured_stories": featured_stories,
        "categories": categories,
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
