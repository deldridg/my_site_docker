from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "Your name",
            "user_email": "Your email",
            "text": "Your comment"
        }

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"