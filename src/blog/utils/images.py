from __future__ import annotations

import logging
from io import BytesIO
from pathlib import Path
from typing import Iterable, Mapping

from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.db.models.fields.files import ImageFieldFile
from PIL import Image

logger = logging.getLogger(__name__)

WEBP_VARIANT_WIDTHS: Mapping[str, int] = {"1x": 1280, "2x": 2048}
WEBP_QUALITY = 82


def _variant_name(original_name: str, label: str) -> str:
    """Return the storage path for a derived variant."""
    path = Path(original_name)
    variant = f"{path.stem}@{label}.webp"
    return str(path.with_name(variant)).replace("\\", "/")


def _resize_image(image: Image.Image, target_width: int) -> Image.Image:
    """Resize an image preserving aspect ratio, avoiding upscaling."""
    width, height = image.size
    if width <= target_width:
        return image.copy()
    ratio = target_width / float(width)
    new_height = int(height * ratio)
    return image.resize((target_width, new_height), Image.LANCZOS)


def delete_webp_variants(
    original_name: str,
    storage: Storage,
    labels: Iterable[str] | None = None,
) -> None:
    """Remove existing derived variants for a given original image."""
    for label in labels or WEBP_VARIANT_WIDTHS.keys():
        variant_name = _variant_name(original_name, label)
        try:
            if storage.exists(variant_name):
                storage.delete(variant_name)
        except Exception:  # pragma: no cover - storage backend specific
            logger.exception("Failed deleting variant %s", variant_name)


def generate_webp_variants(
    image_field: ImageFieldFile,
    widths: Mapping[str, int] | None = None,
) -> list[str]:
    """
    Generate WebP variants (1x/2x) for an ImageFieldFile.

    Returns a list of storage paths that were generated.
    """
    if not image_field or not image_field.name:
        return []

    widths = widths or WEBP_VARIANT_WIDTHS
    storage = image_field.storage
    generated: list[str] = []

    try:
        image_field.open()
        base_image = Image.open(image_field)
        base_image.load()
        base_image = base_image.convert("RGB")
    except Exception:
        logger.exception("Failed opening featured image for conversion")
        return []

    try:
        for label, width in widths.items():
            variant_name = _variant_name(image_field.name, label)
            try:
                resized = _resize_image(base_image, width)
                buffer = BytesIO()
                resized.save(buffer, format="WEBP", quality=WEBP_QUALITY, method=6)
                delete_webp_variants(image_field.name, storage, labels=[label])
                storage.save(variant_name, ContentFile(buffer.getvalue()))
                buffer.close()
                generated.append(variant_name)
            except Exception:  # pragma: no cover - Pillow/storage specific
                logger.exception(
                    "Failed generating %s variant for %s", label, image_field.name
                )
    finally:
        base_image.close()
        image_field.close()
    return generated


def get_variant_urls(
    image_field: ImageFieldFile,
    labels: Iterable[str] | None = None,
) -> dict[str, str]:
    """Return available variant URLs keyed by label."""
    if not image_field or not image_field.name:
        return {}
    labels = tuple(labels or WEBP_VARIANT_WIDTHS.keys())
    storage = image_field.storage
    urls: dict[str, str] = {}
    for label in labels:
        variant_name = _variant_name(image_field.name, label)
        try:
            if storage.exists(variant_name):
                urls[label] = storage.url(variant_name)
        except Exception:  # pragma: no cover
            logger.exception("Failed resolving URL for %s", variant_name)
    return urls


__all__ = [
    "WEBP_VARIANT_WIDTHS",
    "delete_webp_variants",
    "generate_webp_variants",
    "get_variant_urls",
]
