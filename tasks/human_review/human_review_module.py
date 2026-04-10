def review_case(decision: dict, context_data: dict) -> dict:
    if decision.get("label") == "REVIEW":
        # Mock human review deciding it is safe.
        return {"label": "SAFE", "confidence": 1.0, "source": "HUMAN"}
    return decision
