from __future__ import annotations

from typing import Any, Callable


def success(data: Any) -> dict:
    return {"status": "success", "data": data}


def error(message: str, *, source: str = "system", data: Any | None = None) -> dict:
    # Guarantee normalized classification fields even on errors.
    if is_classification(data):
        payload = data
    else:
        payload = classification(label="ERROR", confidence=0.0, source=source, details=data)

    res: dict[str, Any] = {"status": "error", "data": payload}
    if message:
        res["message"] = message
    return res


def classification(*, label: str, confidence: float, source: str, **extra: Any) -> dict:
    payload: dict[str, Any] = {
        "label": str(label),
        "confidence": float(confidence),
        "source": str(source),
    }
    payload.update(extra)
    return payload


def is_module_response(obj: Any) -> bool:
    return isinstance(obj, dict) and obj.get("status") in {"success", "error"} and "data" in obj


def is_classification(obj: Any) -> bool:
    return (
        isinstance(obj, dict)
        and isinstance(obj.get("label"), str)
        and isinstance(obj.get("source"), str)
        and isinstance(obj.get("confidence"), (int, float))
    )


def safe_call(name: str, fn: Callable[..., dict], *args: Any, **kwargs: Any) -> dict:
    try:
        res = fn(*args, **kwargs)
        if not is_module_response(res):
            return error(f"{name} returned invalid response shape", source=name, data=res)
        return res
    except Exception as e:
        return error(f"{name} raised: {type(e).__name__}: {e}", source=name)
