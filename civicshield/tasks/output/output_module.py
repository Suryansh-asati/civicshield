def generate_report(final_result: dict, post_data: dict) -> dict:
    report = {
        "Post": post_data.get("id", "unknown_id"),
        "Label": final_result.get("label", "UNKNOWN"),
        "Confidence": final_result.get("confidence", 0.0),
        "Source": final_result.get("source", "SYSTEM"),
        "OriginalText": post_data.get("text", "")
    }
    return {"label": "COMPLETED", "confidence": 1.0, "report": report}
