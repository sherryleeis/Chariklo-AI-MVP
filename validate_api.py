#!/usr/bin/env python3
"""
Quick API Key Validator for Chariklo
Run this script to test if your API key is working correctly.
"""

import os
import sys
from dotenv import load_dotenv

def test_api_key():
    print("🔍 Testing Chariklo API Connection...")
    print("=" * 40)
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    # Check if key exists
    if not api_key:
        print("❌ No API key found in .env file")
        print("💡 Add ANTHROPIC_API_KEY=your_key_here to .env")
        return False
    
    print(f"✓ API key found: {api_key[:15]}...")
    
    # Test import
    try:
        from anthropic import Anthropic
        print("✓ Anthropic package imported")
    except ImportError:
        print("❌ Anthropic package not installed")
        print("💡 Run: pip install anthropic")
        return False
    
    # Test API call
    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=20,
            messages=[{"role": "user", "content": "Say 'API works!'"}]
        )
        
        result = response.content[0].text.strip()
        print(f"✅ SUCCESS! Response: {result}")
        print("\n🎉 Your API key is working correctly!")
        print("🚀 Chariklo is ready to run!")
        return True
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        
        error_str = str(e).lower()
        if "authentication" in error_str:
            print("\n💡 Fix: Get a valid API key from console.anthropic.com")
            print("💡 Make sure your account has credits")
        elif "rate limit" in error_str:
            print("\n💡 Fix: Wait a few minutes and try again")
        else:
            print(f"\n💡 Unexpected error: {e}")
        
        return False

if __name__ == "__main__":
    if test_api_key():
        print("\n✨ Ready to start Chariklo with: streamlit run main.py")
    else:
        print("\n📖 See API_SETUP.md for detailed setup instructions")
        sys.exit(1)
