
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import ListView
from django.views import View
from django.views.generic.edit import CreateView

from .models import Post, Tag
from .forms import CommentForm, UpdatePostForm

# Create your views here.
#posts = data_frame.to_dict(orient="records")

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        latest_posts = queryset[:3]
        return latest_posts
    
class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"

    tag = None

    def get_queryset(self):
        tag_id = self.kwargs.get("tag_id")
        queryset = super().get_queryset().order_by("-date")
        if tag_id:
            tag = Tag.objects.get(id=tag_id)
            post_list = queryset.filter(tag=tag_id)
            self.tag = tag
        else:
            post_list = queryset
        return post_list
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

class PostDetailView(View):

    def is_saved_post(self, request, post_id):

        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_post = post_id in request.session.get("stored_posts")
        else:
            is_saved_post = False
        return is_saved_post

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "comment_form": CommentForm(),
            "is_saved_for_later": self.is_saved_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(request.path) #reverse("post-detail-page"), args=[slug])
        
        context = {
            "post": post,
            "comment_form": comment_form,
            "is_saved_for_later": self.is_saved_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

def post_update(request, id):
    post = Post.objects.get(id=id)
    
    if request.method == 'POST':
        form = UpdatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()

        return redirect('post-detail-page', post.slug)
    
    else:
        form = UpdatePostForm(instance=post)

    return render(request, "blog/post-update.html", {
        'form': form
    })
    
class ReadLaterView(View):

    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(pk__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        print(f"Stored posts: {stored_posts}")

        return HttpResponseRedirect("/")


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })

# def posts(request, tag_id = -1):
#     if tag_id != -1:
#         tag = Tag.objects.get(id=tag_id)
#         all_posts = Post.objects.filter(tag=tag_id).order_by("-date")
#     else:
#         all_posts = Post.objects.all().order_by("-date")
#         tag = ""
#     return render(request, "blog/all-posts.html", {
#         "all_posts": all_posts,
#         "tag": tag
#     })

# def post_detail(request, slug):
#     post = Post.objects.get(slug = slug)
#     return render(request, "blog/post-detail.html", {
#         "post": post,
#         "post_tags": post.tag.all()
#     })