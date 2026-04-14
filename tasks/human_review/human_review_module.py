from __future__ import annotations

from tasks.common import classification, error, is_classification, is_module_response, success


def review_case(decision: dict, context_data: dict) -> dict:
    if is_module_response(decision):
        decision_data = decision.get("data")
    else:
        decision_data = decision

    if not is_classification(decision_data):
        return error("invalid decision input", data={"decision": decision})

    if decision_data.get("label") == "REVIEW":
        # Mock human review deciding it is safe.
        return success(classification(label="SAFE", confidence=1.0, source="human"))

    return success(decision_data)
