import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

try:
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=100,
        messages=[{"role": "user", "content": "Say hi"}]
    )
    print("✅ Claude 3 Sonnet is available!")
    print(response.content[0].text)
except Exception as e:
    print("❌ Claude 3 Sonnet NOT available:")
    print(e)
