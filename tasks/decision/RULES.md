# DECISION Rules

## Constraints
- Ensure accurate mapping of scores to logical outcomes.
- Handle thresholds:
  - `score > 0.7` → HARMFUL
  - `score < 0.4` → SAFE
  - else → REVIEW.

## Edge Cases
- Score exactly matches a threshold boundary.
