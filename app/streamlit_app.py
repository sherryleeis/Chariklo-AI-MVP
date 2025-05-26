import streamlit as st
import sys
import glob
import os
import json
from dotenv import load_dotenv
from typing import Any, List, Dict, Optional

# Load environment variables from .env file
load_dotenv()

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("PYTHONPATH:", sys.path)

from chariklo.chariklo_core import get_chariklo_response, process_audio_commands
from chariklo.memory_system import UserControlledMemory
from reflection_logger import ReflectionLogger, question_bank
from chariklo.chariklo_reflection_tracker import CharikloReflectionTracker
from analyze_transcript import run_full_transcript_analysis


# Initialize session state
if 'memory_system' not in st.session_state:
    st.session_state.memory_system = UserControlledMemory()
    st.session_state.conversation = []
    st.session_state.reflection_logger = ReflectionLogger()
    st.session_state.reflection_tracker = CharikloReflectionTracker()

col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("assets/chariklo_logo.jpg", width=111)
with col_title:
    st.title("Chariklo: AI for Inner Space")

# Force sidebar to open on app load
st.markdown("""
    <style>
        [data-testid="stSidebar"] { min-width: 350px; max-width: 400px; }
        [data-testid="stSidebar"] > div { display: block !important; }
    </style>
    <script>
        window.parent.document.querySelector('section[data-testid="stSidebar"]')?.classList.remove('collapsed');
    </script>
""", unsafe_allow_html=True)

# Memory controls
memory_enabled = st.checkbox("Allow Chariklo to remember our conversations")
st.session_state.memory_system.toggle_memory(memory_enabled)

# Chat interface
def scroll_to_bottom():
    st.markdown("""
        <script>
        window.scrollTo(0, document.body.scrollHeight);
        </script>
    """, unsafe_allow_html=True)

for message in st.session_state.conversation:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"**Chariklo:** {message['content']}", unsafe_allow_html=True)
    else:
        st.markdown(message["content"], unsafe_allow_html=True)

# Clean session state of any debug artifacts
if 'last_debug_assistant_message' in st.session_state:
    del st.session_state.last_debug_assistant_message

# Show completion status if session ended naturally
if st.session_state.get('session_naturally_completed', False):
    st.success("✨ This conversation reached a natural completion point. The space remains open whenever you'd like to return.")
    if st.button("Continue exploring"):
        st.session_state.session_naturally_completed = False
        st.rerun()

# Play bell sound if flagged by process_audio_commands
if st.session_state.get('play_bell', False):
    st.audio('assets/Bell.m4a')
    st.session_state['play_bell'] = False

# Always scroll to bottom after rendering chat
scroll_to_bottom()

def should_ai_respond(conversation: list) -> bool:
    """Return True if the last message is from the user, so AI should respond."""
    return bool(conversation) and conversation[-1]["role"] == "user"

# User input (robust alternation logic)
if user_input := st.chat_input("What's present for you right now?"):
    st.session_state.pending_user_input = user_input
    st.rerun()

# Process pending user input atomically
if "pending_user_input" in st.session_state:
    user_input = st.session_state.pending_user_input
    del st.session_state.pending_user_input
    # Only append if the last message is not already this user input
    if not (st.session_state.conversation and st.session_state.conversation[-1]["role"] == "user" and st.session_state.conversation[-1]["content"] == user_input):
        st.session_state.conversation.append({"role": "user", "content": user_input})
        if 'reflection_logger' in st.session_state:
            st.session_state.reflection_logger.log_ai_reflection('user_input', user_input, user_prompt=user_input)
    # Only respond if last message is from user and NOT a reflection/meta event
    if st.session_state.conversation and st.session_state.conversation[-1]["role"] == "user":
        # Let Chariklo decide how to respond through her own discernment
        response = get_chariklo_response(user_input, st.session_state.conversation, reflection_logger=st.session_state.reflection_logger)
        clean_response = process_audio_commands(response)
        if 'reflection_logger' in st.session_state:
            st.session_state.reflection_logger.log_ai_reflection('assistant_response', clean_response, user_prompt=user_input)
        st.session_state.conversation.append({"role": "assistant", "content": clean_response})
        
        # Analysis and reflection tracking
        analysis = {}
        if 'reflection_tracker' in st.session_state:
            if st.session_state.reflection_tracker.detect_pivot_or_resonance(analysis, clean_response):
                st.session_state.reflection_tracker.log_pivot(analysis, clean_response)
        # Always save session if consent is given (sanitize filename)
        if st.session_state.get('consent_given', False):
            from datetime import datetime
            import re
            folder = 'saved_sessions/'
            os.makedirs(folder, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            safe_timestamp = re.sub(r'[^0-9A-Za-z\-]', '', timestamp)
            filename = os.path.join(folder, f'session_{safe_timestamp}.json')
            session_data = {
                'conversation': st.session_state.conversation,
                'reflections': st.session_state.reflection_logger.get_session_insights()
            }
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
    st.rerun()



# Memory button
if st.button("Mark this moment as important"):
    if st.session_state.conversation:
        last_exchange = st.session_state.conversation[-2:]  # Last user + AI exchange
        st.session_state.memory_system.mark_memory(last_exchange)
        st.success("Moment marked for future conversations")

# Automatic save: every 20 reflections, save to file
if len(st.session_state.reflection_logger.get_session_insights()) > 0 and \
   len(st.session_state.reflection_logger.get_session_insights()) % 20 == 0:
    st.session_state.reflection_logger.save_session_log()

# --- PATCH: Manual Save Button ---
if (
    'reflection_logger' in st.session_state and
    'consent_given' in st.session_state and
    st.session_state.consent_given is False
):
    if st.button('Enable Autosave & Export'):
        from datetime import datetime
        folder = 'saved_sessions/'
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = f'{folder}session_{timestamp}.json'
        session_data = {
            'conversation': st.session_state.conversation,
            'reflections': st.session_state.reflection_logger.get_session_insights()
        }
        os.makedirs(folder, exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        st.success(f'Full conversation and reflections saved as {filename}!')
        st.session_state.consent_given = True
        st.info('Future autosaves and export are now enabled for this session.')
        st.rerun()

# Utility function for getting latest file
def get_latest_file(pattern):
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

# --- PATCH: Update transcript analysis and historical log loading ---
st.sidebar.markdown("### Advanced Transcript Analysis")
if st.sidebar.button("Run Analysis on Latest Session"):
    transcript_path = get_latest_file("saved_sessions/*.txt")
    if transcript_path:
        with open(transcript_path) as f:
            transcript = f.read()
        # Optionally, load historical logs for evolution tracking
        historical_logs = []
        for log_path in glob.glob("saved_sessions/*.json"):
            try:
                with open(log_path) as lf:
                    historical_logs.append(json.load(lf))
            except Exception:
                continue
        analysis_result = run_full_transcript_analysis(transcript, historical_logs)
        st.session_state['last_transcript_analysis'] = analysis_result
        st.sidebar.success("Analysis complete! See main page for results.")
    else:
        st.sidebar.warning("No transcript found in saved_sessions/.")

if 'last_transcript_analysis' in st.session_state:
    st.markdown("## Advanced Transcript Analysis Results")
    result = st.session_state['last_transcript_analysis']
    st.markdown("### Presence & Awareness Patterns")
    st.json(result['deeper_patterns'])
    st.markdown("### User Insight Emergence")
    st.json(result['user_realizations'])
    st.markdown("### Consciousness Evolution Metrics")
    st.json(result['consciousness_evolution'])
    st.markdown("### Development Insights")
    st.json(result['development_insights'])

# 💬 Onboarding + Consent
if "onboarding_complete" not in st.session_state:
    st.session_state.onboarding_complete = False
if "consent_given" not in st.session_state:
    st.session_state.consent_given = None

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
            # Save initial reflections if any, as .json
            if 'reflection_logger' in st.session_state and st.session_state.reflection_logger.get_session_insights():
                from datetime import datetime
                folder = 'saved_sessions/'
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                filename = f'{folder}session_{timestamp}.json'
                st.session_state.reflection_logger.save_session_log(filename=filename)
            st.rerun()
    with col2:
        if st.button("No, do not save any messages"):
            st.session_state.consent_given = False
            st.session_state.onboarding_complete = True
            st.rerun()
    st.stop()
# === DEV-ONLY: Manual Save and Reflective Analysis Sidebar ===
if os.environ.get("CHARIKLO_DEV") == "1":
    st.sidebar.markdown("### Dev Controls")
    if st.sidebar.button('Manual Save Conversation (Dev)', key='manual_save_dev_sidebar'):
        from datetime import datetime
        folder = 'saved_sessions/'
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = f'{folder}session_{timestamp}.json'
        session_data = {
            'conversation': st.session_state.conversation,
            'reflections': st.session_state.reflection_logger.get_session_insights()
        }
        os.makedirs(folder, exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        st.sidebar.success(f'Conversation and reflections saved as {filename}!')
    
    # Add system prompt refinement suggestions
    if st.sidebar.button('Generate Refinement Insights (Dev)', key='refinement_insights_dev'):
        try:
            # Import the analysis modules
            from analyze_reflections import analyze_reflection_patterns, suggest_prompt_refinements
            
            # Get current session reflections
            current_reflections = st.session_state.reflection_logger.get_session_insights()
            
            if current_reflections and len(current_reflections) > 0:
                # Analyze current session patterns
                patterns = analyze_reflection_patterns(current_reflections)
                suggestions = suggest_prompt_refinements(patterns)
                
                if suggestions:
                    st.sidebar.markdown("### Collaborative Refinement Insights")
                    st.sidebar.markdown("*Based on current session reflections:*")
                    for suggestion in suggestions:
                        st.sidebar.write(f"• {suggestion}")
                    
                    # Add pattern summary
                    if patterns.get('counts'):
                        st.sidebar.markdown("### Reflection Patterns Observed")
                        for pattern_type, count in patterns['counts'].items():
                            if count > 0:
                                st.sidebar.write(f"- {pattern_type.replace('_', ' ').title()}: {count}")
                else:
                    st.sidebar.info("Session too brief for refinement insights - continue exploring together")
            else:
                st.sidebar.info("No reflections yet - insights will emerge as conversation develops")
                
        except Exception as e:
            st.sidebar.error(f"Could not generate insights: {e}")
        
    st.sidebar.markdown("### Reflective Events (Dev Only)")
    reflections = st.session_state.reflection_logger.get_session_insights()
    found = False
    if isinstance(reflections, list):
        for ref in reflections:
            # Defensive: only process dicts
            if not isinstance(ref, dict):
                continue
            event_type = ref['type'] if 'type' in ref else ''
            # Only show true reflective events that meet reflection criteria
            if event_type in ('pivot', 'resonance', 'insight', 'user_insight_emergence', 'surprise', 'prediction_interruption'):
                found = True
                snippet = ref['content'] if 'content' in ref else ''
                user_prompt = ref.get('user_prompt', '')
                
                st.sidebar.markdown(f"**{str(event_type).replace('_', ' ').title()}**")
                
                # Show user prompt if available (what triggered this reflection)
                if user_prompt:
                    st.sidebar.markdown(f"*User:* {user_prompt[:100]}{'...' if len(user_prompt) > 100 else ''}")
                
                # Show the reflection content
                st.sidebar.write(str(snippet))
                
                ts = ref['timestamp'] if 'timestamp' in ref else ''
                st.sidebar.markdown(f"<span style='font-size:10px;color:gray'>{str(ts)}</span>", unsafe_allow_html=True)
                st.sidebar.markdown("---")
        if not found:
            st.sidebar.info("No reflective events detected yet.")
    else:
        st.sidebar.info("No reflective events detected yet.")
