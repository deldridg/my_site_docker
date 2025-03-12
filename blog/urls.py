from django.urls import path

from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<int:tag_id>", views.AllPostsView.as_view(), name="post-tag-page"),
    path("posts/read-later", views.ReadLaterView.as_view(), name="read-later"),
    path("posts/<slug:slug>", views.PostDetailView.as_view(), name="post-detail-page"),
    path("posts/<int:id>/update", views.post_update, name="update-post")
]
