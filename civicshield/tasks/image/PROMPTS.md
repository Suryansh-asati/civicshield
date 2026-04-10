# AI Prompts for IMAGE

## Instructions for AI Agent
When extending or modifying the `image` module, ensure:
1. Adherence to structured output (`label`, `confidence`).
2. No hardcoding of configuration values; use settings from `docs/core/CONFIG.md`.
3. Implement proper logging for all inputs, outputs, and errors.
4. Fail gracefully if a prerequisite step was invalid.
