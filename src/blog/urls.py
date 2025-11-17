from django.urls import path

from .views import (
    PostCreateView,
    PostDetailView,
    PostListView,
    PostManageListView,
    PostUpdateView,
)

urlpatterns = [
    # Internal editor workflow (superadmins only)
    path("manage/posts/", PostManageListView.as_view(), name="post_manage_list"),
    path("manage/posts/new/", PostCreateView.as_view(), name="post_create"),
    path("manage/posts/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    # Public blog
    path("", PostListView.as_view(), name="post_list"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
]
