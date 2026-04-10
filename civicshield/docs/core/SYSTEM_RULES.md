# System Rules

1. **Modular Design**: Each component is isolated and reusable.
2. **Deterministic Outputs**: Every module must return its output in the format:
   ```json
   {
     "label": "<string>",
     "confidence": <float between 0 and 1>
   }
   ```
3. **Explainability First**: All decisions must be traceable via logic (thresholds, weights).
4. **Pipeline-Based**: No direct coupling between modules. Everything flows through a central orchestrator.
5. **AI-Assisted Development**: Code must be structured so AI tools can extend it safely.
