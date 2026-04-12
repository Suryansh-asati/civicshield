from tasks.pipeline.pipeline_module import execute_pipeline

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
        print(f"Label: {result.get('Label', 'UNKNOWN')}")
        print(f"Confidence: {float(result.get('Confidence', 0.0)):.4f}")

if __name__ == '__main__':
    run_tests()
