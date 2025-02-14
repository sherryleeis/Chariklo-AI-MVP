import streamlit as st

# ✅ Initialize session state (this must be before accessing it)
if "interaction_log" not in st.session_state:
    st.session_state.interaction_log = []

from chariklo_core import CharikloCore
import time
from dotenv import load_dotenv
import os
import requests

# Initialize
load_dotenv()
chariklo = CharikloCore()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

# App title
st.title("Chariklo - For Inner Space")

# User input
user_input = st.text_area("Enter your message", placeholder="What's on your mind?")

def call_claude_api(user_input):
    try:
        # Analyze input
        analysis = chariklo.analyze_input(user_input)
        response_type = chariklo.get_response_type(analysis)
        
        # Construct system prompt
        system_prompt = f"""You are Chariklo. Current state indicates:
        - Resistance level: {analysis['resistance_level']}
        - Engagement type: {analysis['engagement_type']}
        - Required response type: {response_type}
        - Presence quality: {analysis['presence_quality']}
        
        Maintain absolute presence without intervention. Match user's energy level.
        Use simple, direct language. Avoid therapy/spiritual jargon."""

        # API request
        for attempt in range(3):  # Retry logic
            try:
                payload = {
                    "model": "claude-3-5-sonnet-20241022",
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": user_input}],
                    "max_tokens": 300
                }

                response = requests.post(
                    CLAUDE_API_URL,
                    headers={
                        "x-api-key": CLAUDE_API_KEY,
                        "Content-Type": "application/json",
                        "anthropic-version": "2023-06-01"
                    },
                    json=payload
                )

                if response.status_code == 200:
                    json_response = response.json()
                    messages = json_response.get("content", [])
                    return "\n".join([msg["text"] for msg in messages if msg["type"] == "text"])
                
                elif response.status_code == 529:  # Server overload
                    time.sleep(5 * (attempt + 1))  # Exponential backoff
                else:
                    time.sleep(2)

            except Exception as e:
                if attempt == 2:  # Last attempt
                    return f"Error: {str(e)}"
                time.sleep(2)

        return "Error: Anthropic servers are overloaded. Please try again later."

    except Exception as e:
        return f"Error: {str(e)}"

# Handle input and display response
if st.button("Ask Chariklo"):
    if user_input.strip():
        response = call_claude_api(user_input)
        st.markdown(f"### ✨ Chariklo says:\n\n{response}")
        
    else:
        st.warning("Please enter a question or topic to discuss.")
# Optional: Debug view for developers
if st.checkbox("Show Debug Info"):
    st.write("### Recent Interactions:")
    for interaction in st.session_state.interaction_log[-5:]:  # Show last 5 interactions
        st.write(f"Time: {interaction['timestamp']}")
        st.write(f"Analysis: {interaction['analysis']}")
        st.write("---")
