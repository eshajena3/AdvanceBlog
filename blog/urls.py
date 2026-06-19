from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

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