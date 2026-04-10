# FUSION Rules

## Constraints
- Must handle missing inputs.
- Must log reasoning.
- Use Logic: `final_score = (text_weight * text_confidence) + (image_weight * image_confidence)`.

## Edge Cases
- Only text is provided.
- Only image is provided.
- Missing confidence values.
