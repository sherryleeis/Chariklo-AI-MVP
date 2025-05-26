#!/usr/bin/env python3
"""
Test different Claude models with Chariklo's system prompt
to see how well they maintain presence-based responses.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Import Chariklo's system prompt
try:
    from chariklo_system_prompt import SYSTEM_PROMPT
    print("✓ Loaded Chariklo system prompt")
except ImportError:
    print("❌ Could not load system prompt")
    exit(1)

# Test prompt - something requiring presence and subtlety
test_input = "I've been feeling really stuck lately. Like I'm going through the motions but nothing feels meaningful anymore."

models_to_test = [
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet-20241022", 
    "claude-3-opus-20240229"
]

print("🧪 Testing Chariklo responses across models...")
print("=" * 60)

for model in models_to_test:
    print(f"\n🤖 Testing {model}:")
    print("-" * 30)
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=150,  # Keep responses short for comparison
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": test_input}]
        )
        
        response_text = response.content[0].text.strip()
        print(f"Response: {response_text}")
        
        # Simple analysis
        word_count = len(response_text.split())
        has_question = "?" in response_text
        feels_present = any(word in response_text.lower() for word in ["notice", "feel", "sense", "what's", "how"])
        
        print(f"📊 Analysis: {word_count} words | Question: {has_question} | Presence words: {feels_present}")
        
    except Exception as e:
        print(f"❌ Error with {model}: {e}")

print("\n" + "=" * 60)
print("💡 Recommendation based on results...")
