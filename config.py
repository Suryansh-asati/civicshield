from __future__ import annotations

import os


def _get_bool(name: str, default: bool) -> bool:
	raw = os.getenv(name)
	if raw is None:
		return default
	return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _get_float(name: str, default: float) -> float:
	raw = os.getenv(name)
	if raw is None:
		return default
	try:
		return float(raw)
	except ValueError:
		return default


def _get_int(name: str, default: int) -> int:
	raw = os.getenv(name)
	if raw is None:
		return default
	try:
		return int(raw)
	except ValueError:
		return default


def _get_str(name: str, default: str) -> str:
	raw = os.getenv(name)
	if raw is None:
		return default
	return raw


# ==================== Demo / Flags ====================

DEMO_MODE: bool = _get_bool("DEMO_MODE", False)
"""If enabled: skip OCR + human review; simplify fusion logic."""


# ==================== Thresholds / Fusion ====================

THRESHOLD_HIGH: float = _get_float("THRESHOLD_HIGH", 0.7)
THRESHOLD_LOW: float = _get_float("THRESHOLD_LOW", 0.4)

TEXT_WEIGHT: float = _get_float("TEXT_WEIGHT", 0.6)
IMAGE_WEIGHT: float = _get_float("IMAGE_WEIGHT", 0.4)


# ==================== NLP ====================

NLP_USE_HF_MODEL: bool = _get_bool("NLP_USE_HF_MODEL", True)
NLP_HF_MODEL_NAME: str = _get_str(
	"NLP_HF_MODEL_NAME",
	"Hate-speech-CNERG/bert-base-uncased-hatexplain",
)
NLP_HF_DEVICE: int = _get_int("NLP_HF_DEVICE", -1)  # -1 CPU, 0 GPU
NLP_TRUNCATION: bool = _get_bool("NLP_TRUNCATION", True)
