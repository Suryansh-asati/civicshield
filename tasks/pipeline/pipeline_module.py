from __future__ import annotations

import datetime
import logging
import os
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


_LOGGER_CONFIGURED = False


def _get_pipeline_logger() -> logging.Logger:
    global _LOGGER_CONFIGURED
    logger = logging.getLogger("civicshield.pipeline")
    if _LOGGER_CONFIGURED:
        return logger

    logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
    logger.propagate = False

    try:
        os.makedirs("logs", exist_ok=True)
        date_str = datetime.date.today().isoformat()
        log_path = os.path.join("logs", f"pipeline_{date_str}.log")
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except Exception:
        # If file logging cannot be configured, keep console-only behavior.
        pass

    _LOGGER_CONFIGURED = True
    return logger

def execute_pipeline(payload: dict) -> dict:
    stage_log: list[dict] = []

    file_logger = _get_pipeline_logger()

    def log(stage: str, msg: str) -> None:
        print(f"[PIPELINE] {stage}: {msg}")
        try:
            file_logger.info(f"[{stage}] {msg}")
        except Exception:
            pass

    def log_debug(stage: str, msg: str) -> None:
        if config.DEBUG:
            print(f"[PIPELINE][DEBUG] {stage}: {msg}")
            try:
                file_logger.debug(f"[{stage}] {msg}")
            except Exception:
                pass

    def record(stage: str, res: dict) -> None:
        stage_log.append({"stage": stage, "status": res.get("status"), "message": res.get("message")})

    # 1) Input
    log("INPUT", "running...")
    log_debug("INPUT", f"input: {payload}")
    input_res = safe_call("input", process_input, payload)
    record("input", input_res)
    if input_res.get("status") == "error":
        log("INPUT", f"ERROR: {input_res.get('message', 'unknown error')}")
    log_debug("INPUT", f"output: {input_res}")

    base_payload = {}
    if input_res.get("status") == "success":
        base_payload = (input_res.get("data") or {}).get("payload") or {}

    # 2) Preprocessing
    log("PREPROCESSING", "running...")
    log_debug("PREPROCESSING", f"input: {base_payload}")
    prep_res = safe_call("preprocessing", clean_data, base_payload)
    record("preprocessing", prep_res)
    if prep_res.get("status") == "error":
        log("PREPROCESSING", f"ERROR: {prep_res.get('message', 'unknown error')}")
    log_debug("PREPROCESSING", f"output: {prep_res}")

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
        log_debug("OCR", f"input: {image}")
        ocr_res = safe_call("ocr", extract_text, image)
        record("ocr", ocr_res)
        if ocr_res.get("status") == "error":
            log("OCR", f"ERROR: {ocr_res.get('message', 'unknown error')}")
        log_debug("OCR", f"output: {ocr_res}")

        if ocr_res.get("status") == "success":
            extracted_text = (ocr_res.get("data") or {}).get("extracted_text") or ""
            if extracted_text:
                # Add separator to preserve original text.
                text = (text + "\n\n[OCR]\n" + extracted_text).strip()

    # 4) NLP (optional)
    nlp_res = None
    if text:
        log("NLP", "running...")
        log_debug("NLP", f"input: {text}")
        nlp_res = safe_call("nlp", analyze_text, text)
        record("nlp", nlp_res)
        if nlp_res.get("status") == "error":
            log("NLP", f"ERROR: {nlp_res.get('message', 'unknown error')}")
        log_debug("NLP", f"output: {nlp_res}")
    else:
        log("NLP", "skipped (no text)")

    # 5) Image
    image_res = None
    if image:
        log("IMAGE", "running...")
        log_debug("IMAGE", f"input: {image}")
        image_res = safe_call("image", analyze_image, image)
        record("image", image_res)
        if image_res.get("status") == "error":
            log("IMAGE", f"ERROR: {image_res.get('message', 'unknown error')}")
        log_debug("IMAGE", f"output: {image_res}")
    else:
        log("IMAGE", "skipped (no image)")

    # 6) Fusion
    log("FUSION", "running...")
    log_debug("FUSION", f"input: nlp={nlp_res} image={image_res}")
    fused_res = safe_call("fusion", fuse_results, nlp_res, image_res)
    record("fusion", fused_res)
    if fused_res.get("status") == "error":
        log("FUSION", f"ERROR: {fused_res.get('message', 'unknown error')}")
    log_debug("FUSION", f"output: {fused_res}")

    # 7) Decision
    log("DECISION", "running...")
    log_debug("DECISION", f"input: {fused_res}")
    decision_res = safe_call("decision", make_decision, fused_res)
    record("decision", decision_res)
    if decision_res.get("status") == "error":
        log("DECISION", f"ERROR: {decision_res.get('message', 'unknown error')}")
    log_debug("DECISION", f"output: {decision_res}")

    # 8) Human review
    final_res = decision_res
    if config.DEMO_MODE:
        log("HUMAN_REVIEW", "skipped (DEMO_MODE=true)")
    else:
        log("HUMAN_REVIEW", "running...")
        log_debug("HUMAN_REVIEW", f"input: decision={decision_res} context={cleaned_payload}")
        final_res = safe_call("human_review", review_case, decision_res, cleaned_payload)
        record("human_review", final_res)
        if final_res.get("status") == "error":
            log("HUMAN_REVIEW", f"ERROR: {final_res.get('message', 'unknown error')}")
        log_debug("HUMAN_REVIEW", f"output: {final_res}")

    # 9) Output
    log("OUTPUT", "running...")
    log_debug("OUTPUT", f"input: final={final_res} payload={payload}")
    output_res = safe_call("output", generate_report, final_res, payload)
    record("output", output_res)
    if output_res.get("status") == "error":
        log("OUTPUT", f"ERROR: {output_res.get('message', 'unknown error')}")
    log_debug("OUTPUT", f"output: {output_res}")

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
