import config

from tasks.common import classification, error, is_classification, is_module_response, success

def make_decision(fused_result: dict) -> dict:
    if is_module_response(fused_result):
        fused_data = fused_result.get("data")
    else:
        fused_data = fused_result

    if not is_classification(fused_data):
        return error("invalid fused_result", source="decision", data={"fused_result": fused_result})

    score = float(fused_data.get("confidence", 0.0))
    
    if score > config.THRESHOLD_HIGH:
        label = "HARMFUL"
    elif score < config.THRESHOLD_LOW:
        label = "SAFE"
    else:
        label = "REVIEW"
        
    return success(classification(label=label, confidence=score, source="decision"))
