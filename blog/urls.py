from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="blog-home"),
     path(
        "<slug:slug>/",
        views.post_detail,
        name="post-detail",
    ),
]