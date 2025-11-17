from __future__ import annotations

from datetime import timedelta
from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.test.client import Client
from django.urls import reverse, reverse_lazy
from django.utils import timezone, translation

from blog.models import Post


# Utility to populate all required localized fields (post.py/modeltranslation style)
def set_localized_post_fields(
    post: Post,
    title: str | None = None,
    slug: str | None = None,
    content: str | None = None,
) -> None:
    """Populate all localized fields on a Post instance for tests."""
    # Required by PostForm clean and save (post.py), also by modeltranslation expectations
    setattr(post, "title_en", title if title else post.title or "EN")
    setattr(post, "title_uk", "УКР " + (post.title or "Title"))
    setattr(post, "slug_en", slug if slug else post.slug or "slug-en")
    setattr(post, "slug_uk", "ua-" + (post.slug or "slug"))
    setattr(
        post,
        "content_en",
        content if content is not None else (post.content or "English content"),
    )
    setattr(post, "content_uk", "Ukrainian content")
    post.save()


@pytest.mark.django_db
def test_post_list_view_shows_only_published_posts(client: Client) -> None:
    now = timezone.now()

    post = Post.objects.create(
        title="Visible post",
        slug="visible-post",
        content="",
        published_at=now - timedelta(days=1),
    )
    set_localized_post_fields(
        post, title="Visible post EN", slug="visible-post-en", content="English content"
    )
    # Draft and future posts
    draft_post = Post.objects.create(
        title="Draft",
        slug="draft-post",
        content="",
        published_at=None,
    )
    set_localized_post_fields(draft_post)
    future_post = Post.objects.create(
        title="Future",
        slug="future-post",
        content="",
        published_at=now + timedelta(days=1),
    )
    set_localized_post_fields(future_post)
    url = reverse("post_list")
    response = client.get(url, secure=True)
    assert response.status_code == 200
    posts = list(response.context["posts"])
    assert {p.slug for p in posts} == {"visible-post"}


@pytest.mark.django_db
def test_post_detail_view_uses_canonical_slug_for_current_language(
    client: Client,
) -> None:
    now = timezone.now()
    post = Post.objects.create(
        title="Localized post",
        slug="base-slug",
        content="",
        published_at=now - timedelta(days=1),
    )
    set_localized_post_fields(post, slug="hello-en")
    with translation.override("en"):
        url = reverse("post_detail", kwargs={"slug": "hello-en"})
        response = client.get(url, secure=True)
    assert response.status_code == 200
    assert response.context["post"].pk == post.pk


@pytest.mark.django_db
def test_post_detail_view_redirects_cross_language_slug_to_current_language(
    client: Client,
) -> None:
    now = timezone.now()
    post = Post.objects.create(
        title="Localized post",
        slug="base-slug",
        content="",
        published_at=now - timedelta(days=1),
    )
    set_localized_post_fields(post, slug="hello-en")
    # Manually override the Ukrainian slug to be different
    post.slug_uk = "hello-uk"
    post.save()
    with translation.override("en"):
        url = reverse("post_detail", kwargs={"slug": "hello-uk"})
        response = client.get(url, secure=True)
    assert response.status_code == 301
    assert response.headers["Location"].endswith(
        reverse("post_detail", kwargs={"slug": "hello-en"})
    )


@pytest.mark.django_db
def test_post_detail_view_returns_404_for_future_publication_date(
    client: Client,
) -> None:
    now = timezone.now()
    post = Post.objects.create(
        title="Future post",
        slug="future-base",
        content="",
        published_at=now + timedelta(days=1),
    )
    set_localized_post_fields(post, slug="future-en")
    post.slug_uk = "future-uk"
    post.save()
    with translation.override("en"):
        url = reverse("post_detail", kwargs={"slug": "future-en"})
        response = client.get(url, secure=True)
    assert response.status_code == 404


# -------------------------
# Tests for post_create.py --
# -------------------------


@pytest.mark.django_db
def test_superuser_required_mixin_allows_superuser_request(rf: Any) -> None:
    """Allows requests from authenticated superuser."""
    from blog.views.post_create import SuperuserRequiredMixin

    class DummyView(SuperuserRequiredMixin):
        request = None

    user = get_user_model().objects.create_user(
        username="super", password="x", is_superuser=True  # noqa: S106
    )
    req = rf.get("/")
    req.user = user
    view = DummyView()
    view.request = req
    assert view.test_func() is True


@pytest.mark.django_db
def test_superuser_required_mixin_rejects_non_superuser(rf: Any) -> None:
    """Rejects non-superuser or anonymous requests."""
    from blog.views.post_create import SuperuserRequiredMixin

    class DummyView(SuperuserRequiredMixin):
        request = None

    # Authenticated but not superuser
    user = get_user_model().objects.create_user(
        username="user", password="x"  # noqa: S106
    )
    req = rf.get("/")
    req.user = user
    view = DummyView()
    view.request = req
    assert view.test_func() is False

    # Anonymous
    class DummyUser:
        is_authenticated = False
        is_superuser = False

    req_anon = rf.get("/")
    req_anon.user = DummyUser()
    view.request = req_anon
    assert view.test_func() is False


@pytest.mark.django_db
def test_superuser_required_mixin_handle_no_permission_redirects_message(
    rf: Any,
) -> None:
    """handle_no_permission should add error message and redirect."""

    from django.contrib.messages.storage.cookie import CookieStorage

    from blog.views.post_create import SuperuserRequiredMixin

    class DummyView(SuperuserRequiredMixin):
        request = None

    req = rf.get("/")
    # Attach a cookie-based message storage backend to avoid relying on
    # session configuration details in settings.
    setattr(req, "_messages", CookieStorage(req))
    view = DummyView()
    view.request = req
    resp = view.handle_no_permission()
    assert isinstance(resp, HttpResponseRedirect)
    assert str(resp.url) == str(reverse_lazy("admin:login"))
    # Error message is present. (Should be set.)
    messages = list(req._messages)
    assert any("superuser" in m.message for m in messages)


@pytest.mark.django_db
def test_post_manage_list_view_requires_superuser(client: Client) -> None:
    """Manage list view: only accessible by authenticated superuser."""

    url = reverse("post_manage_list")
    resp = client.get(url, secure=True)
    assert resp.status_code in (302, 301)
    assert str(reverse_lazy("admin:login")) in str(resp.url)


@pytest.mark.django_db
def test_post_manage_list_view_as_superuser(
    client: Client, django_user_model: Any
) -> None:

    user = django_user_model.objects.create_user(
        "sup", password="pw", is_superuser=True  # noqa: S106
    )
    client.force_login(user)
    url = reverse("post_manage_list")
    resp = client.get(url, secure=True)
    assert resp.status_code == 200
    assert "posts" in resp.context
    assert hasattr(resp.context["posts"], "__iter__")


@pytest.mark.django_db
def test_post_create_view_requires_superuser(client: Client) -> None:
    """PostCreateView: only accessible by superuser."""

    url = reverse("post_create")
    resp = client.get(url, secure=True)
    assert resp.status_code in (301, 302)
    assert str(reverse_lazy("admin:login")) in str(resp.url)


@pytest.mark.django_db
def test_post_create_view_get_and_post_as_superuser(
    client: Client, django_user_model: Any
) -> None:

    user = django_user_model.objects.create_user(
        "superadmin", password="pw", is_superuser=True  # noqa: S106
    )
    client.force_login(user)
    url = reverse("post_create")

    resp = client.get(url, secure=True)
    assert resp.status_code == 200
    assert "form" in resp.context
    # All required localized fields for PostForm, reflecting post.py clean
    data = {
        "title": "Test Title",
        "slug": "test-title",
        "content": "Initial content",
        "title_en": "Test Title EN",
        "title_uk": "Тестова назва УКР",
        "slug_en": "test-title-en",
        "slug_uk": "test-title-uk",
        "content_en": "English test content",
        "content_uk": "Ukrainian test content",
    }
    resp2 = client.post(url, data, secure=True, follow=True)
    assert resp2.status_code == 200
    assert Post.objects.filter(slug="test-title").exists()
    msgs = list(get_messages(resp2.wsgi_request))
    assert any("created successfully" in m.message.lower() for m in msgs)


@pytest.mark.django_db
def test_post_update_view_requires_superuser(
    client: Client, django_user_model: Any
) -> None:

    user = django_user_model.objects.create_user(
        "u1", password="pw", is_superuser=False  # noqa: S106
    )
    client.force_login(user)
    # Create a post (as admin, via db)
    post = Post.objects.create(
        title="t1",
        slug="s1",
        content="c",
        published_at=None,
    )
    set_localized_post_fields(post)
    url = reverse("post_update", args=[post.pk])
    resp = client.get(url, secure=True)
    assert resp.status_code in (301, 302)
    assert str(reverse_lazy("admin:login")) in str(resp.url)


@pytest.mark.django_db
def test_post_update_view_get_and_post_as_superuser(
    client: Client, django_user_model: Any
) -> None:

    user = django_user_model.objects.create_user(
        "root", password="pw", is_superuser=True  # noqa: S106
    )
    client.force_login(user)
    post = Post.objects.create(
        title="Old Title",
        slug="old-slug",
        content="Hi!",
        published_at=None,
    )
    set_localized_post_fields(
        post, title="Old Title EN", slug="old-slug-en", content="Old English Content"
    )
    url = reverse("post_update", args=[post.pk])
    resp = client.get(url, secure=True)
    assert resp.status_code == 200
    assert "form" in resp.context
    assert resp.context["form"].instance.pk == post.pk

    # Need to set all required localized and core fields for PostForm/post.py
    data = {
        "title": "New Title",
        "slug": "old-slug",
        "content": "Edited content",
        "title_en": "New Title EN",
        "title_uk": "Новий заголовок УКР",
        "slug_en": "new-title-en",
        "slug_uk": "new-title-uk",
        "content_en": "Edited English content",
        "content_uk": "Редагований український контент",
    }
    resp2 = client.post(url, data, follow=True, secure=True)
    post.refresh_from_db()
    assert post.title == "New Title"
    assert post.content == "Edited content"
    msgs = list(get_messages(resp2.wsgi_request))
    assert any("updated successfully" in m.message.lower() for m in msgs)
    assert resp2.status_code == 200


@pytest.mark.django_db
def test_manage_list_pagination_for_superuser(
    client: Client, django_user_model: Any
) -> None:

    user = django_user_model.objects.create_user(
        "suser", password="pw", is_superuser=True  # noqa: S106
    )
    client.force_login(user)
    for i in range(25):
        p = Post.objects.create(
            title=f"Post {i}",
            slug=f"slug-{i}",
            content="c",
        )
        set_localized_post_fields(
            p, title=f"Post {i} EN", slug=f"slug-{i}-en", content=f"EN {i}"
        )
    url = reverse("post_manage_list")
    resp = client.get(url, secure=True)
    assert resp.status_code == 200
    posts = resp.context["posts"]
    assert hasattr(posts, "paginator")
    assert posts.paginator.count == 25
    assert posts.paginator.num_pages >= 2
