from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator

from .models import Category, Post


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

    paginator = Paginator(posts, 3)      # 3 posts per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query,
    }

    return render(request, "blog/home.html", context)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)

    posts = Post.objects.filter(
        category=category,
        status="Published",
    ).order_by("-created_at")

    return render(
        request,
        "blog/category_posts.html",
        {
            "category": category,
            "posts": posts,
        },
    )


def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status="Published",
    )

    related_posts = (
        Post.objects.filter(
            category=post.category,
            status="Published",
        )
        .exclude(id=post.id)
        .order_by("-created_at")[:3]
    )

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "related_posts": related_posts,
        },
    )


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    posts = Post.objects.filter(
        tags__slug=slug,
        status="Published",
    ).order_by("-created_at")

    return render(
        request,
        "blog/tag_posts.html",
        {
            "tag": tag,
            "posts": posts,
        },
    )