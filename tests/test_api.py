import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

# Check if API key is loaded correctly
if not CLAUDE_API_KEY:
    print("Error: CLAUDE_API_KEY not found. Make sure your .env file is set up correctly.")
    exit()

# Prepare test payload
payload = {
    "model": "claude-3-5-sonnet-20241022",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 50
}

# Send request
response = requests.post(
    CLAUDE_API_URL,
    headers={
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    },
    json=payload
)

# Print response
print(f"Status Code: {response.status_code}")
print("Response:", response.text)
