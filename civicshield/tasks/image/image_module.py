def analyze_image(image_bytes) -> dict:
    if not image_bytes:
        return {"label": "NO_IMAGE", "confidence": 1.0}
    # Mock output
    if "bad_image" in image_bytes:
        return {"label": "HARMFUL", "confidence": 0.85}
    return {"label": "SAFE", "confidence": 0.8} # typical false safe or valid safe
