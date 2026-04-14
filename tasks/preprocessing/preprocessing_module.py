from __future__ import annotations

from tasks.common import classification, error, success


def clean_data(data: dict) -> dict:
    if not isinstance(data, dict):
        return error("data must be a dict", source="preprocessing", data={"data": data})

    cleaned = data.copy()
    if "text" in cleaned and isinstance(cleaned["text"], str):
        cleaned["text"] = cleaned["text"].strip()

    return success({**classification(label="CLEANED", confidence=1.0, source="preprocessing"), "payload": cleaned})
