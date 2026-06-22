from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from taggit.models import Tag
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Category, Post
from .forms import CommentForm


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
    recent_posts = Post.objects.filter(status="Published").order_by("-created_at")[:5]
    context = {
        "page_obj": page_obj,
        "query": query,
        "recent_posts": recent_posts,
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
        status="Published"
    )

    comments = post.comments.filter(active=True)

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()

            return redirect("post-detail", slug=post.slug)

    else:

        form = CommentForm()

    related_posts = (
        Post.objects.filter(
            category=post.category,
            status="Published"
        )
        .exclude(pk=post.pk)
        .order_by("-created_at")[:3]
    )
    recent_posts = Post.objects.filter(
        status="Published"
    ).exclude(pk=post.pk).order_by("-created_at")[:5]

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "related_posts": related_posts,
        "recent_posts": recent_posts,
    }

    return render(request, "blog/post_detail.html", context)


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
@login_required
def like_post(request, slug):

    post = get_object_or_404(Post, slug=slug)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("post-detail", slug=slug)

@login_required
def dashboard(request):

    posts = Post.objects.filter(
        author=request.user
    ).order_by("-created_at")

    context = {
        "posts": posts,
    }

    return render(
        request,
        "blog/dashboard.html",
        context,
    )