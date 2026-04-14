# TODO: Implement logic based on docs/core/PIPELINE_SPEC.md

from __future__ import annotations

from tasks.common import classification, error

def start_ui() -> dict:
    """
    Provides CLI or UI interface.
    Returns: {"label": "INTERFACE_RUNNING", "confidence": 1.0}
    """
    return error(
        "interface module not implemented",
        data=classification(label="NOT_IMPLEMENTED", confidence=0.0, source="interface"),
    )
