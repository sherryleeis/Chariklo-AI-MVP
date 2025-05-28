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
import chariklo_option_palette

st.title("🌿 Chariklo Test App is Running")


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
    st.session_state.consent_given = None

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

# Option Palette and Tone Archive Display
with st.expander("🎨 Option Palette & Tone Archive (for inspiration)", expanded=True):
    palette = chariklo_option_palette.get_chariklo_option_palette()
    st.markdown("#### Option Palette (Response Inspiration)")
    st.json({k: v for k, v in palette.items() if k != 'tone_archive'})
    st.markdown("#### Tone Archive (All Fragments)")
    st.json(palette.get('tone_archive', []))

# 🌿 Process Input + Defer Analysis to Next Cycle
if user_input := st.chat_input("What's on your mind?"):
    st.session_state.pending_input = user_input
    st.rerun()

# 🔁 Bell + Response Handling
if "pending_input" in st.session_state:
    user_input = st.session_state.pending_input
    analysis = chariklo.analyze_input(user_input)
    response = st.session_state.get("pending_response")

    # ✅ Only generate response once
    if response is None:
        response = chariklo.generate_response(analysis)
        st.session_state.pending_response = response
        if analysis.get("offers_bell"):
            st.session_state["__chariklo_last_offered_bell"] = True

    chariklo_logger.info(
        f"🔔 Bell Debug — offered: {st.session_state.get('__chariklo_last_offered_bell')}, "
        f"user said yes: {chariklo.detect_user_accepts_sound(user_input, 'bell')}"
    )

    if st.session_state.get("__chariklo_last_offered_bell") and chariklo.detect_user_accepts_sound(user_input, "bell"):
        st.button("Preparing bell...", key="pre_bell_button", disabled=True)
        st.audio("Bell.m4a", format="audio/m4a")
        chariklo_logger.info("🔔 Playing bell sound after user consent.")
        time.sleep(2)
        st.session_state["__chariklo_last_offered_bell"] = False

    # Always append to the log for UI display (regardless of consent)
    st.session_state.interaction_log.append({
        "user": user_input,
        "chariklo": response
    })

    del st.session_state["pending_input"]
    del st.session_state["pending_response"]
    st.rerun()


# 🔊 Bell Playback Test
st.markdown("### 🔔 Manual Bell Test")
if st.button("Play the bell manually"):
    st.audio("Bell.m4a", format="audio/m4a")

# 💬 Display chat history
st.markdown("### Conversation")

for i, entry in enumerate(st.session_state.interaction_log):
    show_feedback = st.session_state.consent_given is True  # Only show if user consented
    st.markdown(f"**You:** {entry['user']}", unsafe_allow_html=True)
    st.markdown(f"**Chariklo:** {entry['chariklo']}", unsafe_allow_html=True)

    if show_feedback:
        feedback_col1, feedback_col2, _ = st.columns([1, 1, 6])
        with feedback_col1:
            if st.button("", key=f"thumbs_up_{i}", help="Mark this response as helpful 👍"):
                st.session_state.interaction_log[i]["feedback"] = "positive"
                # Save feedback to file
                feedback_folder = Path("feedback")
                feedback_folder.mkdir(exist_ok=True)
                feedback_data = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "thumbs_up",
                    "user": entry['user'],
                    "chariklo": entry['chariklo'],
                    "session": st.session_state.get('session_id', None)
                }
                with open(feedback_folder / f"feedback_{datetime.now().strftime('%Y%m%d-%H%M%S')}_{i}.json", "w") as f:
                    json.dump(feedback_data, f, indent=2, ensure_ascii=False)
                st.success("Thank you. If you'd like to share what felt clear or helpful, you're welcome to.")

        with feedback_col2:
            if st.button("", key=f"thumbs_down_{i}", help="Mark this response as not helpful 👎"):
                st.session_state.interaction_log[i]["feedback"] = "negative"
                # Save feedback to file
                feedback_folder = Path("feedback")
                feedback_folder.mkdir(exist_ok=True)
                feedback_data = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "thumbs_down",
                    "user": entry['user'],
                    "chariklo": entry['chariklo'],
                    "session": st.session_state.get('session_id', None)
                }
                with open(feedback_folder / f"feedback_{datetime.now().strftime('%Y%m%d-%H%M%S')}_{i}.json", "w") as f:
                    json.dump(feedback_data, f, indent=2, ensure_ascii=False)
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

# 💾 Manual Save Option (even if consent was not given at start)
if st.session_state.interaction_log:
    with st.expander("⬇️ Manual Save Conversation (TXT)", expanded=False):
        st.download_button(
            label="Download as TXT (Manual Save)",
            data="\n\n".join(
                f"You: {entry['user']}\nChariklo: {entry['chariklo']}"
                for entry in st.session_state.interaction_log
            ),
            file_name="chariklo_transcript_manual.txt",
            mime="text/plain"
        )

# Auto-save
if st.session_state.consent_given and st.session_state.interaction_log:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder = Path("saved_sessions")
    folder.mkdir(exist_ok=True)
    filename_txt = folder / f"session_{timestamp}.txt"
    filename_json = folder / f"session_{timestamp}.json"

    from chariklo.chariklo_core import run_presence_priming_reflection
    shift_events, reflection_log = run_presence_priming_reflection()

    # Save TXT with YAML block
    with open(filename_txt, "w") as f:
        f.write("# --- Presence Priming Log ---\n\n")
        f.write("primed_on:\n")
        for chapter in shift_events:
            f.write(f"  - {chapter}\n")
        f.write("\nresonance_log:\n")
        for entry in reflection_log:
            f.write(f"  - \"{entry}\"\n")
        f.write("\n# ----------------------------\n\n")
        for entry in st.session_state.interaction_log:
            f.write(f"You: {entry['user']}\n")
            f.write(f"Chariklo: {entry['chariklo']}\n\n")

    # Save JSON with priming_log at top level
    session_json = {
        "primed_on": shift_events,
        "resonance_log": reflection_log,
        "interaction_log": st.session_state.interaction_log
    }
    with open(filename_json, "w") as f_json:
        json.dump(session_json, f_json, indent=2, ensure_ascii=False)
