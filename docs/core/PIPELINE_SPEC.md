# Pipeline Specification

### Pipeline Behavior Rules:
- OCR runs only if an image exists.
- OCR text must be appended to original text.
- NLP always runs if text exists.
- Image model runs only if an image exists.
- Fusion must combine available outputs.
- Decision must always return final classification.
