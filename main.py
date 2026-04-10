import sys
import os
import json

# Add the project root to sys.path to allow imports from civicshield
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from civicshield.tasks.pipeline.pipeline_module import execute_pipeline

def run_tests():
    payloads = [
        {
            "id": "post_1",
            "text": "This is a completely safe and normal message.",
            "image": None
        },
        {
            "id": "post_2",
            "text": "I absolutely hate this, it is so offensive!",
            "image": None
        },
        {
            "id": "post_3",
            "text": "Check out this picture.",
            "image": "bad_image"
        },
        {
            "id": "post_4",
            "text": "A borderline offensive joke here.", # Will trigger intermediate score
            "image": "normal_image"
        }
    ]

    print("--- CivicShield Pipeline Execution ---")
    for p in payloads:
        print(f"\nProcessing Post: {p['id']}")
        result = execute_pipeline(p)
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    run_tests()
