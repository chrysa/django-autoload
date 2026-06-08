"""Shop API routes — discovered by autodiscover_urls("api")."""

from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from django.urls import path


def list_products(request: HttpRequest) -> JsonResponse:
    """Return a stub list of products."""
    return JsonResponse({"products": ["widget", "gadget"]})


urlpatterns = [
    path("shop/products/", list_products, name="shop-products"),
]
