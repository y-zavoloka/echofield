from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..forms import PostForm
from ..models import Post


class PostCreateView(UserPassesTestMixin, CreateView):
    """
    Class-based view for creating blog posts.
    Only accessible to superusers.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("blog:post_list")

    def test_func(self) -> bool:
        """
        Test function to check if user is a superuser.
        Returns True if user is authenticated and is a superuser.
        """
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def form_valid(self, form: PostForm) -> HttpResponse:
        """
        Set the author of the post to the current user before saving.
        """
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)

    def handle_no_permission(self) -> HttpResponseRedirect:
        """
        Handle cases where user doesn't have permission.
        """
        messages.error(self.request, "You must be a superuser to create posts.")
        return HttpResponseRedirect(reverse_lazy("admin:login"))
