from django.db.models import Q
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView

from blog.translation import PostTranslationOptions
from ..models import Post
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import get_language

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 20

    def get_queryset(self):
        return (
            Post.objects.filter(status="published")
            .order_by("-published_at", "-created_at")
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Post.objects.filter(status="published")
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            slug = self.kwargs["slug"]
            post = Post.objects.filter(Q(slug_en=slug) | Q(slug_uk=slug)).first()
            if post:
                lang = get_language()
                return redirect("post_detail", slug=getattr(post, f"slug_{lang}"))
            raise
