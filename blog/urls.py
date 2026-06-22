from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "create/",
        views.create_post,
        name="create-post",
    ),

    path(
        "edit/<slug:slug>/",
        views.PostUpdateView.as_view(),
        name="edit-post",
    ),

    path(
        "delete/<slug:slug>/",
        views.delete_post,
        name="delete-post",
    ),

    path(
        "category/<slug:slug>/",
        views.category_posts,
        name="category-posts",
    ),

    path(
        "tag/<slug:slug>/",
        views.tag_posts,
        name="tag-posts",
    ),

    path(
        "like/<slug:slug>/",
        views.like_post,
        name="like-post",
    ),

    path(
        "<slug:slug>/",
        views.post_detail,
        name="post-detail",
    ),
]