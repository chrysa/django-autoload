"""Blog API routes — discovered by autodiscover_urls("api")."""

from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from django.urls import path


def list_posts(request: HttpRequest) -> JsonResponse:
    """Return a stub list of blog posts."""
    return JsonResponse({"posts": ["hello-world", "second-post"]})


urlpatterns = [
    path("blog/posts/", list_posts, name="blog-posts"),
]
