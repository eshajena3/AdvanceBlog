from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import Post, Category


def home(request):
    query = request.GET.get("q")

    posts = Post.objects.filter(status="Published")

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        )

    posts = posts.order_by("-created_at")

    context = {
        "posts": posts,
        "query": query,
    }

    return render(request, "blog/home.html", context)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)

    posts = Post.objects.filter(
        category=category,
        status="Published"
    ).order_by("-created_at")

    context = {
        "category": category,
        "posts": posts,
    }

    return render(request, "blog/category_posts.html", context)

def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status="Published"
    )

    related_posts = (
        Post.objects.filter(
            category=post.category,
            status="Published"
        )
        .exclude(id=post.id)[:3]
    )

    context = {
        "post": post,
        "related_posts": related_posts,
    }

    return render(request, "blog/post_detail.html", context)