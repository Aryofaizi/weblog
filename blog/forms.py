from django.forms import ModelForm  # model -> form
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text", "author", "status"]
