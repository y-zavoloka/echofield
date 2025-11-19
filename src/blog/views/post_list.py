from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from ..models import Post
from ..utils.seo import build_alternate_links, build_canonical_url


class PostListView(ListView):
    model = Post
    template_name: str = "post_list.html"
    context_object_name: str = "posts"
    paginate_by: int = 20

    def get_queryset(self) -> QuerySet[Post]:
        """Return posts that are considered published based on their date only."""
        return Post.public.published().prefetch_related("categories")

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context.setdefault(
            "meta_title", _("EchoField — %(label)s") % {"label": _("Posts")}
        )
        context.setdefault(
            "meta_description",
            _(
                "EchoField publishes bilingual essays, field notes, and research updates."
            ),
        )
        canonical = build_canonical_url(self.request)
        context["canonical_url"] = canonical
        context["alternate_links"] = build_alternate_links(self.request)
        return context
