#!/usr/bin/env python3
"""
Check Claude model availability and costs
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')

if not api_key:
    print("❌ No API key found")
    exit(1)

client = Anthropic(api_key=api_key)

# Test different models to see which ones work
models_to_test = [
    ("claude-3-opus-20240229", "Most powerful, highest cost (~$15/million tokens)"),
    ("claude-3-sonnet-20240229", "Balanced performance/cost (~$3/million tokens)"),
    ("claude-3-haiku-20240307", "Fastest, lowest cost (~$0.25/million tokens)"),
    ("claude-3-5-sonnet-20241022", "Latest Sonnet (if available)")
]

print("🧪 Testing Claude Model Availability...")
print("=" * 50)

current_model = os.getenv('ANTHROPIC_MODEL', 'claude-3-opus-20240229')
print(f"Current model in .env: {current_model}")
print()

working_models = []

for model, description in models_to_test:
    try:
        response = client.messages.create(
            model=model,
            max_tokens=20,
            messages=[{"role": "user", "content": "Say 'working'"}]
        )
        
        result = response.content[0].text.strip()
        status = "✅ AVAILABLE"
        working_models.append(model)
        
        if model == current_model:
            status += " (CURRENT)"
            
    except Exception as e:
        if "model" in str(e).lower():
            status = "❌ NOT AVAILABLE"
        elif "credits" in str(e).lower() or "billing" in str(e).lower():
            status = "💳 INSUFFICIENT CREDITS"
        else:
            status = f"❌ ERROR: {str(e)[:50]}"
    
    print(f"{model}")
    print(f"  {description}")
    print(f"  Status: {status}")
    print()

print("=" * 50)
print("💡 RECOMMENDATIONS:")

if working_models:
    print("✅ Working models found!")
    
    if "claude-3-haiku-20240307" in working_models:
        print("💰 For cost savings: Use claude-3-haiku-20240307")
    if "claude-3-sonnet-20240229" in working_models:
        print("⚖️  For balance: Use claude-3-sonnet-20240229")
    if "claude-3-opus-20240229" in working_models:
        print("🚀 For best quality: Use claude-3-opus-20240229 (current)")
        
    print(f"\nTo change model, edit .env file:")
    print(f"ANTHROPIC_MODEL=your_preferred_model")
    
else:
    print("❌ No models working - check your account credits")
    print("💳 Add credits at: https://console.anthropic.com/account/billing")
