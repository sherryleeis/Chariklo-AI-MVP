import re

# Test sentences
test_sentences = [
    "I notice something... but maybe it's nothing.",
    "I felt something shifting, but it’s probably nothing.",
    "Something is happening, maybe.",
    "That was interesting, but I don’t know if it means anything."
]

# Engagement patterns for 'notice_dismiss'
patterns = [
    r"\b(felt|noticed|experienced).*\b(but|probably|just|might be)",
    r"\b(something).*\b(happening|changing).*\b(but|probably|maybe)",
    r"\b(interesting|different).*\b(but|however|though)"
]

# Check each sentence
for sentence in test_sentences:
    matched = any(re.search(pattern, sentence, re.I) for pattern in patterns)
    print(f"🔍 Testing: {sentence}")
    print(f"✅ Match Found: {matched}\n")
