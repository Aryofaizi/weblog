from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views import generic
from django.urls import reverse_lazy

from .models import Post
from .forms import PostForm


def get_posts():
    return Post.objects.all()


class PostListView(generic.ListView):
    # model = Post
    template_name = "blog/post_list.html"
    context_object_name = "post_list"

    def get_queryset(self):
        return Post.objects.filter(status="pub").order_by("-datetime_modified")


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = "blog/create_post.html"


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create_post.html"


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("post_list")
    # success_url = reverse("post_list")
    # def get_success_url(self):
    #     return reverse("post_list")


# def home_page_view(request):
#     return render(request, "blog/home.html")

# functional view
# class-based view
# def post_list_view(request):
#     post_list = Post.objects.filter(status="pub").order_by("-datetime_modified")
#     return render(request, "blog/post_list.html", {"post_list": post_list})

# def post_detail_view(request, pk):
#     # try:
#     #     post = Post.objects.get(pk=pk)
#     # except ObjectDoesNotExist:
#     # except Post.DoesNotExist:
#     #     post = None
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, "blog/post_detail.html", {"post": post})

# def post_create_view(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("post_list")
#
#     else:
#         form = PostForm()
#     return render(request, "blog/create_post.html", context={"form": form})

# def post_update_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form = PostForm(request.POST or None, instance=post)
#
#     if form.is_valid():
#         form.save()
#         return redirect("post_list")
#
#     return render(request, "blog/create_post.html", context={"form": form})

# def post_delete_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         post.delete()
#         return redirect("post_list")
#
#     return render(request, "blog/post_delete.html", context={"post": post})
