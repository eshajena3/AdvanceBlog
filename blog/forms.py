from django import forms
from .models import Comment,Post


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["name", "email", "body"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your Name"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Your Email"
            }),

            "body": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Write your comment..."
            }),
        }
class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            "title",
            "category",
            "featured_image",
            "content",
            "tags",
            "status",
        ]