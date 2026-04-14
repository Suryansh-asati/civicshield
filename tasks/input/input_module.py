from __future__ import annotations

from tasks.common import classification, error, success


def process_input(payload: dict) -> dict:
    if not isinstance(payload, dict):
        return error("payload must be a dict", source="input", data={"payload": payload})

    # Minimal validation for demo stability.
    post_id = payload.get("id")
    if post_id is None:
        return error("missing required field: id", source="input", data={"payload": payload})

    data = {
        **classification(label="VALID", confidence=1.0, source="input"),
        "payload": payload,
    }
    return success(data)
