from __future__ import annotations

import config

from tasks.common import is_module_response, safe_call
from tasks.input.input_module import process_input
from tasks.preprocessing.preprocessing_module import clean_data
from tasks.ocr.ocr_module import extract_text
from tasks.nlp.nlp_module import analyze_text
from tasks.image.image_module import analyze_image
from tasks.fusion.fusion_module import fuse_results
from tasks.decision.decision_module import make_decision
from tasks.human_review.human_review_module import review_case
from tasks.output.output_module import generate_report

def execute_pipeline(payload: dict) -> dict:
    stage_log: list[dict] = []

    def log(stage: str, msg: str) -> None:
        print(f"[PIPELINE] {stage}: {msg}")

    def record(stage: str, res: dict) -> None:
        stage_log.append({"stage": stage, "status": res.get("status"), "message": res.get("message")})

    # 1) Input
    log("INPUT", "running...")
    input_res = safe_call("input", process_input, payload)
    record("input", input_res)
    log("INPUT", f"output: {input_res}")

    base_payload = {}
    if input_res.get("status") == "success":
        base_payload = (input_res.get("data") or {}).get("payload") or {}

    # 2) Preprocessing
    log("PREPROCESSING", "running...")
    prep_res = safe_call("preprocessing", clean_data, base_payload)
    record("preprocessing", prep_res)
    log("PREPROCESSING", f"output: {prep_res}")

    cleaned_payload = base_payload
    if prep_res.get("status") == "success":
        cleaned_payload = (prep_res.get("data") or {}).get("payload") or base_payload

    text = cleaned_payload.get("text") or ""
    image = cleaned_payload.get("image")

    # 3) OCR (optional)
    ocr_res = None
    if config.DEMO_MODE:
        log("OCR", "skipped (DEMO_MODE=true)")
    elif image:
        log("OCR", "running...")
        ocr_res = safe_call("ocr", extract_text, image)
        record("ocr", ocr_res)
        log("OCR", f"output: {ocr_res}")

        if ocr_res.get("status") == "success":
            extracted_text = (ocr_res.get("data") or {}).get("extracted_text") or ""
            if extracted_text:
                # Add separator to preserve original text.
                text = (text + "\n\n[OCR]\n" + extracted_text).strip()

    # 4) NLP (optional)
    nlp_res = None
    if text:
        log("NLP", "running...")
        nlp_res = safe_call("nlp", analyze_text, text)
        record("nlp", nlp_res)
        log("NLP", f"output: {nlp_res}")
    else:
        log("NLP", "skipped (no text)")

    # 5) Image
    image_res = None
    if image:
        log("IMAGE", "running...")
        image_res = safe_call("image", analyze_image, image)
        record("image", image_res)
        log("IMAGE", f"output: {image_res}")
    else:
        log("IMAGE", "skipped (no image)")

    # 6) Fusion
    log("FUSION", "running...")
    fused_res = safe_call("fusion", fuse_results, nlp_res, image_res)
    record("fusion", fused_res)
    log("FUSION", f"output: {fused_res}")

    # 7) Decision
    log("DECISION", "running...")
    decision_res = safe_call("decision", make_decision, fused_res)
    record("decision", decision_res)
    log("DECISION", f"output: {decision_res}")

    # 8) Human review
    final_res = decision_res
    if config.DEMO_MODE:
        log("HUMAN_REVIEW", "skipped (DEMO_MODE=true)")
    else:
        log("HUMAN_REVIEW", "running...")
        final_res = safe_call("human_review", review_case, decision_res, cleaned_payload)
        record("human_review", final_res)
        log("HUMAN_REVIEW", f"output: {final_res}")

    # 9) Output
    log("OUTPUT", "running...")
    output_res = safe_call("output", generate_report, final_res, payload)
    record("output", output_res)
    log("OUTPUT", f"output: {output_res}")

    if output_res.get("status") != "success":
        # As a last resort, return a consistent error payload.
        return {
            "status": "error",
            "data": {
                "label": "UNKNOWN",
                "confidence": 0.0,
                "source": "pipeline",
                "report": None,
                "stages": stage_log,
            },
            "message": output_res.get("message", "output stage failed"),
        }

    data = output_res.get("data") or {}
    # Final pipeline output: consistent wrapper and include stage summaries.
    return {
        "status": "success",
        "data": {
            **(data.get("final") or {}),
            "report": data.get("report"),
            "stages": stage_log,
        },
    }
