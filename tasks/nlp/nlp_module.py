try:
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
except ModuleNotFoundError:  # Optional dependency
    AutoModelForSequenceClassification = None
    AutoTokenizer = None
    pipeline = None

import config

from tasks.common import classification, error, success

MODEL_NAME = config.NLP_HF_MODEL_NAME

# Lazy initialized classifier to avoid loading model at import time.
_classifier = None
_hf_failure_logged = False


def _load_classifier():
    global _classifier
    if pipeline is None or AutoTokenizer is None or AutoModelForSequenceClassification is None:
        _classifier = False
        raise RuntimeError("transformers is not installed")
    if _classifier is False:
        raise RuntimeError("HuggingFace model unavailable in this environment")
    if _classifier is None:
        try:
            if not config.NLP_USE_HF_MODEL:
                raise RuntimeError("NLP_USE_HF_MODEL is disabled")
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            model = AutoModelForSequenceClassification.from_pretrained(
                MODEL_NAME,
                use_safetensors=False,
            )
            _classifier = pipeline(
                "text-classification",
                model=model,
                tokenizer=tokenizer,
                device=config.NLP_HF_DEVICE,
            )
        except Exception:
            _classifier = False
            raise
    return _classifier


def _fallback_rule_based(text: str) -> dict:
    lowered = text.lower()
    if any(token in lowered for token in ["hate", "kill", "offensive", "slur"]):
        return classification(label="HARMFUL", confidence=0.65, source="nlp_fallback")
    return classification(label="SAFE", confidence=0.55, source="nlp_fallback")


def analyze_text(text: str) -> dict:
    if not text or not text.strip():
        return success(classification(label="NO_TEXT", confidence=1.0, source="nlp"))

    label_map = {
        "LABEL_0": "HARMFUL",
        "LABEL_1": "SAFE",
        "LABEL_2": "OFFENSIVE",
        "hate speech": "HARMFUL",
        "normal": "SAFE",
        "offensive": "OFFENSIVE",
    }

    try:
        classifier = _load_classifier()
        result = classifier(text, truncation=config.NLP_TRUNCATION)[0]
        raw_label = str(result.get("label", "")).strip()
        mapped_label = label_map.get(raw_label, "UNKNOWN")
        return success(
            classification(
                label=mapped_label,
                confidence=float(result.get("score", 0.0)),
                source=MODEL_NAME,
                raw_label=raw_label,
            )
        )
    except Exception:
        # Keep pipeline runnable even if model download/runtime fails.
        import traceback

        global _hf_failure_logged
        if not _hf_failure_logged:
            _hf_failure_logged = True
            print(f"[NLP] HuggingFace model failed; using fallback. model={MODEL_NAME}")
            traceback.print_exc(limit=2)
        return success(_fallback_rule_based(text))

