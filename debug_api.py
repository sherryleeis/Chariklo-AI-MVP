#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

print("=== Debugging Chariklo API Connection ===")

# Load environment variables
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')

print(f"✓ API Key loaded: {bool(api_key)}")
if api_key:
    print(f"✓ API Key length: {len(api_key)}")
    print(f"✓ API Key format: {api_key[:15]}...")

# Check anthropic installation
try:
    import anthropic
    print(f"✓ Anthropic version: {anthropic.__version__}")
except ImportError as e:
    print(f"❌ Anthropic import failed: {e}")
    print("Installing anthropic...")
    os.system("pip install anthropic")
    import anthropic

# Test basic API connection
try:
    from anthropic import Anthropic
    client = Anthropic(api_key=api_key)
    print("✓ Client created successfully")
    
    # Simple test call
    print("Testing API call...")
    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Using a cheaper/faster model for testing
        max_tokens=50,
        messages=[{"role": "user", "content": "Hello, respond with just 'API working'"}]
    )
    
    response_text = response.content[0].text
    print(f"✅ SUCCESS! Response: {response_text}")
    
except Exception as e:
    print(f"❌ API Error: {type(e).__name__}")
    print(f"❌ Details: {str(e)}")
    
    # Let's try to understand the error better
    error_str = str(e).lower()
    if "api key" in error_str or "authentication" in error_str:
        print("\n🔍 DIAGNOSIS: API Key Issue")
        print("- Check if your API key is valid")
        print("- Verify it has sufficient credits")
        print("- Make sure it's the correct Anthropic API key")
    elif "model" in error_str:
        print("\n🔍 DIAGNOSIS: Model Issue")
        print("- The specified model might not be available")
        print("- Try a different model like claude-3-sonnet-20240229")
    elif "rate" in error_str:
        print("\n🔍 DIAGNOSIS: Rate Limit")
        print("- You've hit the API rate limit")
        print("- Wait a few minutes and try again")
    else:
        print(f"\n🔍 DIAGNOSIS: Unknown error")
        print("Full error for debugging:")
        print(repr(e))

print("\n=== Test Complete ===")
