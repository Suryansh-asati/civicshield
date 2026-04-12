from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

MODEL_NAME = "Hate-speech-CNERG/bert-base-uncased-hatexplain"

# Lazy initialized classifier to avoid loading model at import time.
_classifier = None


def _load_classifier():
    global _classifier
    if _classifier is False:
        raise RuntimeError("HuggingFace model unavailable in this environment")
    if _classifier is None:
        try:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            model = AutoModelForSequenceClassification.from_pretrained(
                MODEL_NAME,
                use_safetensors=False,
            )
            _classifier = pipeline(
                "text-classification",
                model=model,
                tokenizer=tokenizer,
            )
        except Exception:
            _classifier = False
            raise
    return _classifier


def _fallback_rule_based(text: str) -> dict:
    lowered = text.lower()
    if any(token in lowered for token in ["hate", "kill", "offensive", "slur"]):
        return {"label": "HARMFUL", "confidence": 0.65, "source": "NLP_FALLBACK"}
    return {"label": "SAFE", "confidence": 0.55, "source": "NLP_FALLBACK"}


def analyze_text(text: str) -> dict:
    if not text or not text.strip():
        return {"label": "NO_TEXT", "confidence": 1.0, "source": "NLP"}

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
        result = classifier(text, truncation=True)[0]
        raw_label = str(result.get("label", "")).strip()
        mapped_label = label_map.get(raw_label, "UNKNOWN")
        return {
            "label": mapped_label,
            "confidence": float(result.get("score", 0.0)),
            "source": MODEL_NAME,
            "raw_label": raw_label,
        }
    except Exception:
        # Keep pipeline runnable even if model download/runtime fails.
        return _fallback_rule_based(text)

