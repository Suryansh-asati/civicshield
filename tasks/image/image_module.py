from __future__ import annotations

from tasks.common import classification, error, success


def analyze_image(image_bytes) -> dict:
    if not image_bytes:
        return success(classification(label="NO_IMAGE", confidence=1.0, source="image"))

    # Mock output
    if isinstance(image_bytes, str) and "bad_image" in image_bytes:
        return success(classification(label="HARMFUL", confidence=0.85, source="image"))
    return success(classification(label="SAFE", confidence=0.8, source="image"))
