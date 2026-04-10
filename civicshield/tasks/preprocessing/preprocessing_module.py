def clean_data(data: dict) -> dict:
    cleaned = data.copy()
    if 'text' in cleaned and isinstance(cleaned['text'], str):
        cleaned['text'] = cleaned['text'].strip()
    return {"label": "CLEANED", "confidence": 1.0, "data": cleaned}
