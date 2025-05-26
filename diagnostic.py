import streamlit as st
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Chariklo API Diagnostic", page_icon="🔍")

st.title("🔍 Chariklo API Diagnostic")

# Load environment
load_dotenv()

st.markdown("## 🔧 Environment Check")

# Check API key
api_key = os.getenv('ANTHROPIC_API_KEY')
if api_key:
    st.success(f"✅ API Key found: {api_key[:15]}...")
    st.info(f"🔍 Key length: {len(api_key)} characters")
else:
    st.error("❌ No API key found!")

# Check model
model = os.getenv('ANTHROPIC_MODEL', 'Not set')
st.info(f"🤖 Model: {model}")

# Test API connection
st.markdown("## 🧪 API Connection Test")

if st.button("Test API Connection"):
    if not api_key:
        st.error("❌ No API key to test!")
    else:
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)
            
            with st.spinner("Testing API..."):
                response = client.messages.create(
                    model=model,
                    max_tokens=50,
                    messages=[{"role": "user", "content": "Say 'API test successful'"}]
                )
            
            result = response.content[0].text.strip()
            st.success(f"✅ API Working! Response: {result}")
            
        except Exception as e:
            st.error(f"❌ API Error: {str(e)}")
            
            error_str = str(e).lower()
            if "authentication" in error_str:
                st.warning("🔑 This is an API key authentication issue")
            elif "rate limit" in error_str:
                st.warning("⏱️ Rate limit hit - wait and try again")
            elif "model" in error_str:
                st.warning("🤖 Model not available or misspelled")

# Environment info
st.markdown("## 📍 Environment Info")
st.code(f"""
Platform: {os.name}
Working Directory: {os.getcwd()}
Python Path: {os.environ.get('PYTHONPATH', 'Not set')}
""")

# Show all environment variables starting with ANTHROPIC or CLAUDE
st.markdown("## 🔐 Environment Variables")
for key, value in os.environ.items():
    if key.startswith(('ANTHROPIC', 'CLAUDE')):
        if 'API_KEY' in key:
            display_value = f"{value[:15]}..." if value else "Not set"
        else:
            display_value = value
        st.code(f"{key}={display_value}")

st.markdown("---")
st.markdown("**If this shows API working but main app doesn't, there's a code issue.**")
st.markdown("**If this shows API failing, fix the API key first.**")
