from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="blog-home"),

     path(
        "category/<slug:slug>/",
        views.category_posts,
        name="category-posts",
    ),
     path(
        "<slug:slug>/",
        views.post_detail,
        name="post-detail",
    ),
    path("tag/<slug:slug>/", views.tag_posts, name="tag_posts"),
   
]