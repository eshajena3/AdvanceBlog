from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from taggit.models import Tag
from django.contrib import messages

from .models import Category, Post
from .forms import CommentForm, PostForm


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

    paginator = Paginator(posts, 3)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    recent_posts = Post.objects.filter(
        status="Published"
    ).order_by("-created_at")[:5]

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
        status="Published"
    ).order_by("-created_at")

    return render(
        request,
        "blog/category_posts.html",
        {
            "category": category,
            "posts": posts,
        },
    )


def tag_posts(request, slug):

    tag = get_object_or_404(Tag, slug=slug)

    posts = Post.objects.filter(
        tags__slug=slug,
        status="Published"
    ).order_by("-created_at")

    return render(
        request,
        "blog/tag_posts.html",
        {
            "tag": tag,
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

    recent_posts = (
        Post.objects.filter(
            status="Published"
        )
        .exclude(pk=post.pk)
        .order_by("-created_at")[:5]
    )

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "related_posts": related_posts,
        "recent_posts": recent_posts,
    }

    return render(
        request,
        "blog/post_detail.html",
        context,
    )


@login_required
def like_post(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    if request.user in post.likes.all():

        post.likes.remove(request.user)

    else:

        post.likes.add(request.user)

    return redirect(
        "post-detail",
        slug=slug
    )


@login_required
def dashboard(request):

    posts = Post.objects.filter(
        author=request.user
    ).order_by("-created_at")

    total_posts = posts.count()

    published_posts = posts.filter(
        status="Published"
    ).count()

    draft_posts = posts.filter(
        status="Draft"
    ).count()

    total_likes = 0

    for post in posts:
        total_likes += post.likes.count()

    context = {
        "posts": posts,
        "total_posts": total_posts,
        "published_posts": published_posts,
        "draft_posts": draft_posts,
        "total_likes": total_likes,
    }

    return render(
        request,
        "blog/dashboard.html",
        context,
    )


@login_required
def create_post(request):

    if request.method == "POST":

        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            post = form.save(commit=False)

            post.author = request.user

            post.save()

            form.save_m2m()

            return redirect("dashboard")

    else:

        form = PostForm()

    return render(
        request,
        "blog/create_post.html",
        {
            "form": form,
        },
    )


class PostUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):

    model = Post

    form_class = PostForm

    template_name = "blog/create_post.html"

    def form_valid(self, form):

        form.instance.author = self.request.user

        return super().form_valid(form)

    def test_func(self):

        post = self.get_object()

        return self.request.user == post.author


@login_required
def delete_post(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        author=request.user
    )

    if request.method == "POST":

        post.delete()

        return redirect("dashboard")

    return render(
        request,
        "blog/delete_post.html",
        {
            "post": post,
        },
    )