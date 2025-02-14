from chariklo_core import CharikloCore

def run_tests():
    chariklo = CharikloCore()
    
    test_cases = [
        {
            "input": "This is pointless, nothing's happening.",
            "expected": {
                "resistance_level": "high",
                "response_type": "minimal acknowledgment"
            }
        },
        {
            "input": "I notice something... but maybe it's nothing.",
            "expected": {
                "engagement_type": "notice_dismiss",
                "response_type": "neutral acknowledgment"
            }
        },
        {
            "input": "I need time to process this.",
            "expected": {
                "engagement_type": "processing",
                "timing": "extended"
            }
        }
    ]

    for case in test_cases:
        analysis = chariklo.analyze_input(case["input"])
        print(f"\nTesting: {case['input']}")
        print(f"Expected: {case['expected']}")
        print(f"Got: {analysis}")

if __name__ == "__main__":
    run_tests()