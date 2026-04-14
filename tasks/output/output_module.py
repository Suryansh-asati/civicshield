from __future__ import annotations

from tasks.common import classification, error, is_classification, is_module_response, success


def generate_report(final_result: dict, post_data: dict) -> dict:
    if is_module_response(final_result):
        final_data = final_result.get("data")
    else:
        final_data = final_result

    if not is_classification(final_data):
        return error("invalid final_result", source="output", data={"final_result": final_result})

    report = {
        "post_id": post_data.get("id", "unknown_id"),
        "label": final_data.get("label", "UNKNOWN"),
        "confidence": float(final_data.get("confidence", 0.0)),
        "source": final_data.get("source", "system"),
        "original_text": post_data.get("text", ""),
    }

    return success(
        {
            **classification(label="REPORT", confidence=1.0, source="output"),
            "final": final_data,
            "report": report,
        }
    )
