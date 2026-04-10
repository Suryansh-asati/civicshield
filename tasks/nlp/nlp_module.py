from transformers import pipeline

# Initialize the pipeline lazily
_classifier = None

def analyze_text(text: str) -> dict:
    global _classifier
    
    if not text or not text.strip():
        return {"label": "NO_TEXT", "confidence": 1.0}

    if _classifier is None:
        # Use a model suited for hate speech/offensive/normal classification
        # Hate-speech-CNERG/bert-base-uncased-hatexplain has labels: hate speech, normal, offensive
        _classifier = pipeline("text-classification", model="Hate-speech-CNERG/bert-base-uncased-hatexplain")

    result = _classifier(text)[0]
    
    # Map model labels to CivicShield labels
    # Model labels: 'LABEL_0' (hate speech), 'LABEL_1' (normal), 'LABEL_2' (offensive)
    # Note: Depending on the model version, labels might be names or LABEL_X
    label_map = {
        "LABEL_0": "HARMFUL",
        "LABEL_1": "SAFE",
        "LABEL_2": "OFFENSIVE",
        "hate speech": "HARMFUL",
        "normal": "SAFE",
        "offensive": "OFFENSIVE"
    }
    
    raw_label = result['label']
    mapped_label = label_map.get(raw_label, "UNKNOWN")
    confidence = result['score']
    
    return {"label": mapped_label, "confidence": confidence}

