from __future__ import annotations

import config

from tasks.common import classification, is_classification, is_module_response, success


def _extract_classification(module_res: dict | None) -> dict | None:
    if not module_res:
        return None
    if is_module_response(module_res):
        data = module_res.get("data")
        if is_classification(data):
            return data
        return None
    if is_classification(module_res):
        return module_res
    return None


def fuse_results(nlp_result: dict | None, image_result: dict | None) -> dict:
    nlp = _extract_classification(nlp_result)
    img = _extract_classification(image_result)

    def harm_score(res: dict | None) -> float:
        if not res:
            return 0.0
        label = res.get("label")
        conf = float(res.get("confidence", 0.0))
        if label == "HARMFUL":
            return conf
        if label == "OFFENSIVE":
            return conf * 0.7
        return 0.0

    t_score = harm_score(nlp) if nlp and nlp.get("label") != "NO_TEXT" else 0.0
    i_score = harm_score(img) if img and img.get("label") != "NO_IMAGE" else 0.0

    if config.DEMO_MODE:
        # Simplified fusion for demos: prefer text score, otherwise image score.
        final_score = t_score if t_score > 0.0 else i_score
    else:
        if t_score > 0.0 and i_score > 0.0:
            final_score = (config.TEXT_WEIGHT * t_score) + (config.IMAGE_WEIGHT * i_score)
        elif t_score > 0.0:
            final_score = t_score
        elif i_score > 0.0:
            final_score = i_score
        else:
            final_score = 0.0

    return success(classification(label="FUSED", confidence=final_score, source="fusion"))
