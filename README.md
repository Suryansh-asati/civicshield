# 🛡️ CivicShield

**CivicShield** is a state-of-the-art **Multimodal AI Content Moderation System** designed to detect harmful social media content using a structured, modular, and explainable pipeline.

---

## 🚀 Objective
Build a robust decision-making pipeline that goes beyond simple model predictions by integrating multiple data points (Text, Images, OCR) through a centralized orchestrator.

### Core Capabilities:
*   **Text Analysis (NLP)**: Powered by HuggingFace Transformers for hate speech and offensive content detection.
*   **Image Analysis**: Visual pattern detection for harmful imagery.
*   **OCR**: Extraction of textual content from within images for cross-modal analysis.
*   **Fusion Logic**: Weighted interaction between text and image signals.
*   **Threshold-based Decision System**: Deterministic logic to categorize content or flag for review.
*   **Human-in-the-Loop**: Integrated verification for borderline cases.

---

## 🏗️ Architecture & Pipeline
CivicShield follows a strict, deterministic flow:

`Input → Preprocessing → OCR → NLP → Image Analysis → Fusion → Decision → Human Review → Output`

### Development Philosophy:
1.  **Modular Design**: Every component is isolated and reusable.
2.  **Deterministic Outputs**: Every module returns structured JSON: `{"label": "<string>", "confidence": <float>}`.
3.  **Explainability First**: Decisions are traceable via logic (thresholds, weights) rather than "black-box" conclusions.
4.  **Pipeline-Based**: No direct coupling between modules.

---

## 📂 Project Structure
```text
civicshield/
│
├── docs/               # System-level documentation and rules
│   └── core/
│
├── tasks/              # Individual module implementations
│   ├── input/
│   ├── preprocessing/
│   ├── ocr/
│   ├── nlp/            # HuggingFace Transformers implementation
│   ├── image/
│   ├── fusion/         # Logic-heavy consolidation
│   ├── decision/       # Threshold enforcement
│   ├── human_review/
│   ├── output/
│   ├── pipeline/       # Orchestration logic
│   ├── testing/
│   └── interface/
│
├── main.py             # Entry point / Integration tests
└── requirements.txt    # Project dependencies
```

---

## 🛠️ Getting Started

### Prerequisites
*   Python 3.8+
*   Internet connection (for downloading HuggingFace models on first run)

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the System
Execute the main entry point to run integrated tests across various scenarios (Neutral, Hate, Image-heavy, Borderline):
```bash
python main.py
```

---

## ⚙️ Configuration
The system behavior is controlled via `config.py` (or `docs/core/CONFIG.md`):
*   `THRESHOLD_HIGH = 0.7`: Above this, content is flagged as **HARMFUL**.
*   `THRESHOLD_LOW = 0.4`: Below this, content is marked **SAFE**.
*   `TEXT_WEIGHT = 0.6` / `IMAGE_WEIGHT = 0.4`: Weights for the fusion engine.

---

## 📝 License
This project is developed as part of the CivicShield moderation initiative.
