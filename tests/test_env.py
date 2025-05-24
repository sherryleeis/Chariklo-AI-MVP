import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if the API key is loaded
api_key = os.getenv("ANTHROPIC_API_KEY")

if api_key:
    print(f"✅ API Key Loaded: {api_key[:5]}... (truncated for security)")
else:
    print("❌ ERROR: Anthropic API Key not found. Check your .env file!")
