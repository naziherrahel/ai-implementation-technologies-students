"""Executable input checks for the classroom image-upload service."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError


def load_contract(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check(rule: str, observed: Any, passed: bool) -> dict[str, Any]:
    return {
        "rule": rule,
        "observed": observed,
        "status": "pass" if passed else "error",
    }


def validate_image_upload(
    data: bytes,
    content_type: str | None,
    contract: dict[str, Any],
) -> tuple[list[dict[str, Any]], Image.Image | None, dict[str, Any]]:
    """Validate transport metadata and the image that was actually decoded."""
    checks = [
        check(
            "content_type_allowed",
            content_type,
            content_type in contract["allowed_content_types"],
        ),
        check(
            "upload_size_supported",
            len(data),
            0 < len(data) <= contract["maximum_upload_bytes"],
        ),
    ]

    image: Image.Image | None = None
    metadata: dict[str, Any] = {"bytes": len(data)}

    if data and len(data) <= contract["maximum_upload_bytes"]:
        try:
            decoded = Image.open(BytesIO(data))
            decoded.load()
            metadata.update(
                {
                    "format": decoded.format,
                    "mode": decoded.mode,
                    "width": decoded.width,
                    "height": decoded.height,
                }
            )
            checks.extend(
                [
                    check(
                        "decoded_format_allowed",
                        decoded.format,
                        decoded.format in contract["allowed_decoded_formats"],
                    ),
                    check(
                        "decoded_mode_supported",
                        decoded.mode,
                        decoded.mode in contract["allowed_decoded_modes"],
                    ),
                    check(
                        "dimensions_supported",
                        {"width": decoded.width, "height": decoded.height},
                        decoded.width >= contract["minimum_width"]
                        and decoded.height >= contract["minimum_height"],
                    ),
                ]
            )
            image = decoded.convert("RGB")
        except (UnidentifiedImageError, OSError, ValueError):
            checks.append(check("image_decodes", "decode_failed", False))
    else:
        checks.append(check("image_decodes", "not_attempted", False))

    if image is not None:
        checks.append(check("image_decodes", "decoded", True))

    return checks, image, metadata


def all_checks_pass(checks: list[dict[str, Any]]) -> bool:
    return all(item["status"] == "pass" for item in checks)
