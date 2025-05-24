import streamlit as st
import sys

print("PYTHONPATH:", sys.path)

from chariklo.chariklo_core import get_chariklo_response, process_audio_commands
from chariklo.memory_system import UserControlledMemory
from reflection_logger import ReflectionLogger
from chariklo_reflection_tracker import CharikloReflectionTracker

# Initialize session state
if 'memory_system' not in st.session_state:
    st.session_state.memory_system = UserControlledMemory()
    st.session_state.conversation = []
    st.session_state.reflection_logger = ReflectionLogger()
    st.session_state.reflection_tracker = CharikloReflectionTracker()

st.title("Chariklo: AI for Awareness")

# Memory controls
memory_enabled = st.checkbox("Allow Chariklo to remember our conversations")
st.session_state.memory_system.toggle_memory(memory_enabled)

# Chat interface
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
if user_input := st.chat_input("What's present for you right now?"):
    # Add user message
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    # Get Chariklo response
    response = get_chariklo_response(user_input, st.session_state.conversation)
    # Process any audio commands
    clean_response = process_audio_commands(response)
    # Add AI response
    st.session_state.conversation.append({"role": "assistant", "content": clean_response})
    # Reflection tracking (placeholder logic)
    analysis = None  # If you have access to analysis, pass it here
    if st.session_state.reflection_tracker.detect_pivot_or_resonance(analysis, clean_response):
        st.session_state.reflection_tracker.log_pivot(analysis, clean_response)
    # Refresh to show new messages
    st.rerun()

# Memory button
if st.button("Mark this moment as important"):
    if st.session_state.conversation:
        last_exchange = st.session_state.conversation[-2:]  # Last user + AI exchange
        st.session_state.memory_system.mark_memory(last_exchange)
        st.success("Moment marked for future conversations")
