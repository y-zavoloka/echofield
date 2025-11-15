from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from ..forms.post import PostForm
from ..models import Post


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Mixin restricting access to authenticated superusers only."""

    def test_func(self) -> bool:  # type: ignore[override]
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self) -> HttpResponseRedirect:  # type: ignore[override]
        messages.error(self.request, "You must be a superuser to manage posts.")
        return HttpResponseRedirect(reverse_lazy("admin:login"))


class PostManageListView(SuperuserRequiredMixin, ListView):
    """Internal list of posts for editors (superadmins only)."""

    model = Post
    template_name = "post_manage_list.html"
    context_object_name = "posts"
    paginate_by = 20


class PostCreateView(SuperuserRequiredMixin, CreateView):
    """Custom post creation view with Markdown editor for two languages."""

    model = Post
    form_class = PostForm
    template_name = "post_editor.html"
    success_url = reverse_lazy("post_manage_list")

    def form_valid(self, form: PostForm) -> HttpResponse:  # type: ignore[override]
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)


class PostUpdateView(SuperuserRequiredMixin, UpdateView):
    """Custom post update view with Markdown editor for two languages."""

    model = Post
    form_class = PostForm
    template_name = "post_editor.html"
    success_url = reverse_lazy("post_manage_list")

    def form_valid(self, form: PostForm) -> HttpResponse:  # type: ignore[override]
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)
