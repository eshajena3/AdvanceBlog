from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):

    STATUS = (
        ("Draft", "Draft"),
        ("Published", "Published"),
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    featured_image = models.ImageField(
        upload_to="posts/",
        default="default.jpg"
    )

    content = RichTextField()

    tags = TaggableManager()

    likes = models.ManyToManyField(
        User,
        related_name="blog_posts",
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="Draft"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    name = models.CharField(max_length=100)

    email = models.EmailField()

    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.name}"