from django.conf import settings
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import get_language
from django.views.generic import DetailView

from ..models import Post


def _slug_for_lang(post: Post, lang: str) -> str:
    """
    Get the slug for a post in a specific language.

    Args:
        post: The Post instance to get the slug for
        lang: The language code (e.g., 'en', 'uk')

    Returns:
        The localized slug if available, otherwise falls back to the default slug
    """
    return getattr(post, f"slug_{lang}", None) or post.slug


class PostDetailView(DetailView[Post]):
    """
    Detail view for displaying individual blog posts with multilingual slug support.

    This view handles:
    1. Canonical slug lookup for the current language
    2. Cross-language slug redirects with proper 301 redirects
    3. Fallback to 404 if post is not found in any language
    """

    model = Post
    template_name: str = "post_detail.html"
    context_object_name: str = "post"
    slug_field: str = "slug"
    slug_url_kwarg: str = "slug"

    def get_queryset(self) -> QuerySet[Post]:
        """Return only publicly available posts."""
        return Post.public.all()

    def get(
        self, request: HttpRequest, *args: object, **kwargs: dict[str, object]
    ) -> HttpResponse:
        """
        Handle GET requests with multilingual slug resolution.

        The lookup strategy:
        1. Look for canonical slug in current language
        2. If found but slug doesn't match canonical, redirect to canonical
        3. If not found in current language, look in other languages
        4. If found in other language, redirect to canonical slug for current language
        5. If not found anywhere, raise 404

        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments including 'slug'

        Returns:
            HttpResponse: Either a rendered template or a redirect response

        Raises:
            Http404: If the post is not found in any language
        """
        lang: str = get_language() or settings.LANGUAGE_CODE
        slug = str(self.kwargs[self.slug_url_kwarg])

        # Step 1: Look for canonical post in current language
        exact = Post.public.for_slug(slug, lang=lang).first()
        if exact:
            canonical = _slug_for_lang(exact, lang)
            # Redirect to canonical slug if current slug is not canonical
            if slug != canonical:
                return redirect("post_detail", slug=canonical, permanent=True)
            self.object = exact
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

        # Step 2: Look for post in other languages and redirect to current language canonical
        cross = Post.public.for_slug(slug).first()
        if cross:
            return redirect(
                "post_detail", slug=_slug_for_lang(cross, lang), permanent=True
            )

        # Step 3: Post not found in any language
        raise Http404("Post not found")
