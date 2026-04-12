try:
    from civicshield import config
except ImportError:
    import config

def make_decision(fused_result: dict) -> dict:
    score = fused_result.get("confidence", 0.0)
    
    if score > config.THRESHOLD_HIGH:
        label = "HARMFUL"
    elif score < config.THRESHOLD_LOW:
        label = "SAFE"
    else:
        label = "REVIEW"
        
    return {"label": label, "confidence": score}
