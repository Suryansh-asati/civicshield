from civicshield.tasks.input.input_module import process_input
from civicshield.tasks.preprocessing.preprocessing_module import clean_data
from civicshield.tasks.ocr.ocr_module import extract_text
from civicshield.tasks.nlp.nlp_module import analyze_text
from civicshield.tasks.image.image_module import analyze_image
from civicshield.tasks.fusion.fusion_module import fuse_results
from civicshield.tasks.decision.decision_module import make_decision
from civicshield.tasks.human_review.human_review_module import review_case
from civicshield.tasks.output.output_module import generate_report

def execute_pipeline(payload: dict) -> dict:
    # 1. Input Validation
    input_res = process_input(payload)
    data = input_res.get("data", {})
    
    # 2. Preprocessing
    prep_res = clean_data(data)
    cleaned_data = prep_res.get("data", {})
    
    text = cleaned_data.get("text", "")
    image = cleaned_data.get("image", None)
    
    # 3. OCR (conditionally runs if image exists)
    if image:
        ocr_res = extract_text(image)
        if ocr_res.get("text"):
            text += ocr_res.get("text")
            
    # 4. NLP (conditionally runs if text exists)
    nlp_res = None
    if text:
        nlp_res = analyze_text(text)
        
    # 5. Image Analysis (conditionally runs if image exists)
    image_res = None
    if image:
        image_res = analyze_image(image)
        
    # 6. Fusion
    fused_res = fuse_results(nlp_res, image_res)
    
    # 7. Decision
    decision_res = make_decision(fused_res)
    
    # 8. Human Review (handles REVIEW cases)
    final_res = review_case(decision_res, cleaned_data)
    
    # 9. Output reporting
    output_res = generate_report(final_res, payload)
    
    return output_res.get("report", {})
