from django.db.models.query import QuerySet
from django.views.generic import ListView

from ..models import Post


class PostListView(ListView):
    model = Post
    template_name: str = "post_list.html"
    context_object_name: str = "posts"
    paginate_by: int = 20

    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.filter(status="published").order_by(
            "-published_at", "-created_at"
        )
