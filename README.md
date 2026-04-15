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
*   Python 3.10+ recommended (works with newer Linux distros)
*   Internet connection (first run may download HuggingFace model weights)

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Optional (only if you want to run the `agents/` demo with OpenClaw/CMDOP + Ollama):
```bash
pip install -r requirements-agents.txt
```

Note on Linux: installing `torch` can depend on your CUDA/CPU setup.
If `pip install -r requirements.txt` fails on `torch`, install PyTorch using the official instructions for your platform, then re-run the requirements install.

### Running the System
Execute the main entry point to run integrated tests across various scenarios (Neutral, Hate, Image-heavy, Borderline):
```bash
python main.py
```

Recommended for a clean demo:
```bash
DEMO_MODE=1 python main.py
```

To see stage inputs/outputs (debug mode):
```bash
DEBUG=1 python main.py
```

First-time model download:
- If `transformers`/`torch` are installed and `NLP_USE_HF_MODEL=true`, the first run may download the HuggingFace model specified by `NLP_HF_MODEL_NAME`.
- If the download fails or `transformers` is not installed, the system logs the reason and falls back to a lightweight rule-based classifier (demo-safe backup).

---

## ⚙️ Configuration
The system behavior is controlled via `config.py` (or `docs/core/CONFIG.md`):
*   `THRESHOLD_HIGH = 0.7`: Above this, content is flagged as **HARMFUL**.
*   `THRESHOLD_LOW = 0.4`: Below this, content is marked **SAFE**.
*   `TEXT_WEIGHT = 0.6` / `IMAGE_WEIGHT = 0.4`: Weights for the fusion engine.

Demo flags:
* `DEMO_MODE`: skips OCR + human review; simplifies fusion for stable demos.
* `DEBUG`: prints stage inputs/outputs and NLP tracebacks.

---

## 📝 License
This project is developed as part of the CivicShield moderation initiative.
