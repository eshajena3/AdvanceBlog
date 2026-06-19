from django.shortcuts import render, get_object_or_404
from .models import Post


def home(request):
    posts = Post.objects.filter(status="Published").order_by("-created_at")

    return render(request, "blog/home.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status="Published"
    )

    return render(
        request,
        "blog/post_detail.html",
        {"post": post}
    )