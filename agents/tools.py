def fetch_data():
    return [
        "I hate this community",
        "Everyone is welcome here",
        "We should attack them"
    ]


def analyze_text(text):
    if "hate" in text.lower() or "attack" in text.lower():
        return {"label": "hate", "confidence": 0.9}
    return {"label": "safe", "confidence": 0.2}


def alert_authority(data):
    print("🚨 ALERT:", data)