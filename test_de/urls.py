from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index-page"),
    path("search/", views.search, name="search-page")
]
