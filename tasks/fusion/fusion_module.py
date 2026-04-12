import config

def fuse_results(nlp_result: dict, image_result: dict) -> dict:
    # If a model outputted SAFE, we invert confidence conceptually for "harmfulness" score, 
    # but let's just make a simple mock mapping for the score to work straightforward.
    
    def get_harm_score(res):
        if not res: return 0.0
        if res.get("label") == "HARMFUL": return res.get("confidence", 0.0)
        if res.get("label") == "OFFENSIVE": return res.get("confidence", 0.0) * 0.7
        return 0.0 # SAFE
        
    t_score = get_harm_score(nlp_result)
    i_score = get_harm_score(image_result)
    
    # Weighted average only if both exist, otherwise full weight to the one that exists.
    if nlp_result and image_result and nlp_result.get("label") != "NO_TEXT" and image_result.get("label") != "NO_IMAGE":
        final_score = (config.TEXT_WEIGHT * t_score) + (config.IMAGE_WEIGHT * i_score)
    elif nlp_result and nlp_result.get("label") != "NO_TEXT":
        final_score = t_score
    elif image_result and image_result.get("label") != "NO_IMAGE":
        final_score = i_score
    else:
        final_score = 0.0
        
    return {"label": "FUSED", "confidence": final_score}
