def extract_text(image_bytes) -> dict:
    if not image_bytes:
        return {"label": "NO_IMAGE", "confidence": 1.0, "text": ""}
    return {"label": "OCR_SUCCESS", "confidence": 0.8, "text": " [mock extracted text]"}
