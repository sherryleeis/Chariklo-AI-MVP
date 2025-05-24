import re

thought_patterns = {
    "identification": {
        "patterns": [
            r"(feels like me|I am this|this is me)",
            r"(so strong|overwhelming).*?(feels like me)",
            r"(this is who I am|this defines me)"
        ]
    }
}

test_cases = [
    "This is me.",
    "It feels like me.",
    "This sensation is so strong, it feels like me.",
    "This defines me.",
    "This is who I am."
]

for test in test_cases:
    matched = False
    for pattern in thought_patterns["identification"]["patterns"]:
        if re.search(pattern, test, re.I):
            matched = True
            print(f"✅ Matched: {test} → {pattern}")
            break  # Stop checking if we already found a match

    if not matched:
        print(f"❌ No Match: {test}")
