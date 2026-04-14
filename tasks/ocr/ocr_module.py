from __future__ import annotations

from tasks.common import classification, error, success


def extract_text(image_bytes) -> dict:
    if not image_bytes:
        return success({**classification(label="NO_IMAGE", confidence=1.0, source="ocr"), "extracted_text": ""})

    # Mock OCR output for demo.
    extracted_text = "[mock extracted text]"
    return success(
        {**classification(label="OCR_SUCCESS", confidence=0.8, source="ocr"), "extracted_text": extracted_text}
    )
