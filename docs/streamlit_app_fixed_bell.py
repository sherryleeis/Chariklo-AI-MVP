import streamlit as st
from PIL import Image
from chariklo_core import CharikloCore
import time
from dotenv import load_dotenv
import os
import json
import logging
from datetime import datetime
from pathlib import Path

# ─── Logging Configuration ─────────────────────────────
chariklo_logger = logging.getLogger("chariklo")
chariklo_logger.setLevel(logging.INFO)

# Logo and Header
col1, col2 = st.columns([1, 5])
with col1:
    logo = Image.open("chariklo_logo.jpg")
    st.image(logo, width=80)

with col2:
    st.markdown(
        """
        <div style='display: flex; align-items: center; height: 80px; margin-left: -30px;'>
            <div style='font-size: 275%; font-weight: 600;'>
                Chariklo — <span style='font-style: italic;'>for inner space</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 🌱 Session State Initialization
if "interaction_log" not in st.session_state:
    st.session_state.interaction_log = []

if "onboarding_complete" not in st.session_state:
    st.session_state.onboarding_complete = False

if "consent_given" not in st.session_state:
    st.session_state.consent_given = None  # True, False, or None (pending)

# 💬 Onboarding + Consent
if not st.session_state.onboarding_complete:
    st.markdown("#### Welcome to Chariklo")
    st.markdown("""
    You’re helping refine an AI that we hope will help make room for some quiet —some space— in the deluge of stimulation humans face today. 

    Use this space just as you would any other chat, but Chariklo is meant to be especially helpful in sorting out ideas and challenges in a way that helps bring insight and clarity.

    If anything feels off or especially helpful, you’re invited to click the thumbs up or down or leave a note in the chat. Your reflections are welcome.

    Would you be willing to let Chariklo save an anonymized copy of your session?
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, you may save this session"):
            st.session_state.consent_given = True
            st.session_state.onboarding_complete = True
            st.rerun()

    with col2:
        if st.button("No, do not save any messages"):
            st.session_state.consent_given = False
            st.session_state.onboarding_complete = True
            st.rerun()

    st.stop()

# ✅ Load Chariklo
load_dotenv()
chariklo = CharikloCore()

# 🔍 Send to Chariklo
def call_claude_api(user_input):
    try:
        analysis = chariklo.analyze_input(user_input)

        # Log bell offer + response check
        chariklo_logger.info(
            f"🪵 Bell check — pending: {st.session_state.get('__chariklo_last_offered_bell')}, "
            f"user said yes: {chariklo.detect_user_accepts_sound(user_input, 'bell')}"
        )

        # Check for bell response from user
        if st.session_state.get("__chariklo_last_offered_bell") and chariklo.detect_user_accepts_sound(user_input, "bell"):
            chariklo_logger.info("🔔 Playing bell sound...")
            st.audio("Bell.m4a", format="audio/m4a")
            st.session_state["__chariklo_last_offered_bell"] = False
            return "", analysis

        # Proceed to generate normal response
        response = chariklo.generate_response(analysis)

        if analysis.get("follows_with_silence") is True:
            chariklo_logger.info("⏳ Chariklo is holding silence for 3 seconds...")
            time.sleep(3)

        return response, analysis

    except Exception as e:
        chariklo_logger.error(f"Claude API error: {e}")
        return "⚠️ Claude could not complete this request.", {}

# 🌿 Process Input + Respect Consent
if user_input := st.chat_input("What's on your mind?"):
    analysis = chariklo.analyze_input(user_input)
    st.session_state["__chariklo_last_offered_bell"] = analysis.get("offers_bell", False)
    st.session_state.pending_input = user_input
    st.rerun()

if "pending_input" in st.session_state:
    response, analysis = call_claude_api(st.session_state.pending_input)

    if st.session_state.consent_given:
        st.session_state.interaction_log.append({
            "user": st.session_state.pending_input,
            "chariklo": response
        })
    else:
        st.session_state.interaction_log.append({
            "user": "[input not saved]",
            "chariklo": "[response not saved]"
        })

    del st.session_state["pending_input"]
    st.rerun()

# 💬 Display chat history
st.markdown("### Conversation")

for i, entry in enumerate(st.session_state.interaction_log):
    st.markdown(f"**You:** {entry['user']}", unsafe_allow_html=True)
    st.markdown(f"**Chariklo:** {entry['chariklo']}", unsafe_allow_html=True)

    feedback_col1, feedback_col2, _ = st.columns([1, 1, 6])
    with feedback_col1:
        if st.button("👍", key=f"thumbs_up_{i}"):
            st.session_state.interaction_log[i]["feedback"] = "positive"
            st.success("Thank you. If you'd like to share what felt clear or helpful, you're welcome to.")

    with feedback_col2:
        if st.button("👎", key=f"thumbs_down_{i}"):
            st.session_state.interaction_log[i]["feedback"] = "negative"
            st.warning("Thank you for helping me figure this out. If you can offer any advice on how it could have worked better, it will help with future updates.")

    st.markdown("---")

# Export
if st.session_state.consent_given and st.session_state.interaction_log:
    with st.expander("⬇️ Export conversation", expanded=False):
        st.download_button(
            label="Download as TXT",
            data="\n\n".join(
                f"You: {entry['user']}\nChariklo: {entry['chariklo']}"
                for entry in st.session_state.interaction_log
            ),
            file_name="chariklo_transcript.txt",
            mime="text/plain"
        )

# Auto-save
if st.session_state.consent_given:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder = Path("saved_sessions")
    folder.mkdir(exist_ok=True)
    filename = folder / f"session_{timestamp}.txt"

    with open(filename, "w") as f:
        for entry in st.session_state.interaction_log:
            f.write(f"You: {entry['user']}\n")
            f.write(f"Chariklo: {entry['chariklo']}\n\n")