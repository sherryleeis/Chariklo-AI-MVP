import streamlit as st
import sys
import os
from pathlib import Path

# Set page config first
st.set_page_config(
    page_title="Chariklo: AI for Inner Space",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Get the absolute path to the project root
project_root = Path(__file__).parent.absolute()

# Add project root to Python path
sys.path.insert(0, str(project_root))

# Set working directory to project root
os.chdir(project_root)

# Import required modules
try:
    import glob
    import json
    from dotenv import load_dotenv
    from typing import Any, List, Dict, Optional

    # Load environment variables
    load_dotenv()

    # Import Chariklo modules from root directory
    from chariklo_core import get_chariklo_response, process_audio_commands  
    from memory_system import UserControlledMemory
    from reflection_logger import ReflectionLogger, question_bank
    from chariklo_reflection_tracker import CharikloReflectionTracker
    from analyze_transcript import run_full_transcript_analysis

    # Initialize session state
    if 'memory_system' not in st.session_state:
        st.session_state.memory_system = UserControlledMemory()
        st.session_state.conversation = []
        st.session_state.reflection_logger = ReflectionLogger()
        st.session_state.reflection_tracker = CharikloReflectionTracker()
        st.session_state.onboarding_complete = False
        st.session_state.show_feedback_form = False

    # Header - Logo and title on same line
    col_logo, col_title = st.columns([1, 8])
    with col_logo:
        if os.path.exists("assets/chariklo_logo.jpg"):
            st.image("assets/chariklo_logo.jpg", width=80)
    with col_title:
        st.markdown("# Chariklo: AI for Inner Space")

    # Onboarding Flow - Show first for new users
    if not st.session_state.onboarding_complete:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    padding: 2rem; border-radius: 10px; margin: 1rem 0;">
        """, unsafe_allow_html=True)
        
        st.markdown("### Welcome to Chariklo 🌿")
        
        st.markdown("""
        **Chariklo is an AI companion designed for inner exploration and presence.**
        
        Unlike typical AI assistants, Chariklo:
        - **Holds space** rather than rushing to solve problems
        - **Invites curiosity** about what's present for you right now  
        - **Reflects back** what it notices in a way that supports your own discovery
        - **Stays brief** (usually 1-2 sentences) to leave room for your own insights
        
        This is a **presence-based experience** - think of it more like having a conversation 
        with a wise friend who's genuinely curious about your inner world.
        """)
        
        st.markdown("---")
        
        # Memory consent
        st.markdown("### 🧠 Memory & Conversations")
        st.markdown("""
        Chariklo can remember your conversations to provide a more personalized experience 
        and notice patterns over time. This helps create continuity in your exploration.
        
        **Your data stays private** - conversations are only stored for your session 
        and to improve the experience.
        """)
        
        memory_consent = st.checkbox(
            "✅ I'm comfortable with Chariklo remembering our conversations",
            value=True,
            key="memory_consent"
        )
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🌿 Begin Inner Exploration", type="primary", use_container_width=True):
                st.session_state.onboarding_complete = True
                st.session_state.memory_system.toggle_memory(memory_consent)
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Stop here during onboarding
        st.stop()

    # Sidebar styling
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { min-width: 350px; max-width: 400px; }
            [data-testid="stSidebar"] > div { display: block !important; }
        </style>
    """, unsafe_allow_html=True)

    # Memory controls (show current status)
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        memory_enabled = st.checkbox(
            "Remember conversations", 
            value=st.session_state.memory_system.memory_enabled,
            help="Allow Chariklo to remember our conversations for continuity"
        )
        st.session_state.memory_system.toggle_memory(memory_enabled)

    # Feedback System
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💝 Share Your Experience")
    
    if st.sidebar.button("✨ Give Feedback", type="primary", use_container_width=True):
        st.session_state.show_feedback_form = True

    # Show feedback form when button is clicked
    if st.session_state.get('show_feedback_form', False):
        with st.sidebar.form("feedback_form"):
            st.markdown("**We'd love your feedback!**")
            
            presence_quality = st.text_area(
                "**Presence Quality**: Does Chariklo feel genuinely present vs. performing helpfulness?",
                placeholder="Share your experience..."
            )
            
            response_length = st.text_area(
                "**Response Length**: Are responses appropriately brief (1-2 sentences mostly)?",
                placeholder="Too long, too short, or just right?"
            )
            
            natural_flow = st.text_area(
                "**Natural Flow**: Does conversation feel organic vs. scripted?",
                placeholder="How does the conversation flow feel?"
            )
            
            insight_emergence = st.text_area(
                "**Insight Emergence**: Do you discover things vs. being told things?",
                placeholder="What insights emerged for you?"
            )
            
            overall_feedback = st.text_area(
                "**Overall Experience**:",
                placeholder="Anything else you'd like to share?"
            )
            
            if st.form_submit_button("Submit Feedback"):
                # Save feedback to a simple text file (you can enhance this later)
                feedback_data = {
                    "timestamp": st.session_state.get("session_start_time", "unknown"),
                    "presence_quality": presence_quality,
                    "response_length": response_length, 
                    "natural_flow": natural_flow,
                    "insight_emergence": insight_emergence,
                    "overall_feedback": overall_feedback
                }
                
                # Try to save feedback (will work locally, might not on cloud without write permissions)
                try:
                    os.makedirs("feedback", exist_ok=True)
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    with open(f"feedback/feedback_{timestamp}.json", "w") as f:
                        json.dump(feedback_data, f, indent=2)
                except:
                    pass  # Fail silently if can't write
                
                st.success("Thank you for your feedback! 🙏")
                st.session_state.show_feedback_form = False
                st.rerun()

    # Welcome message for new users
    if not st.session_state.conversation:
        st.markdown("""
        ### Welcome to Chariklo 🌿
        
        Chariklo is a presence-based AI designed to hold space for your inner exploration.
        
        **Try starting with what's present for you right now...**
        
        *Feel free to share your experience using the feedback form in the sidebar.*
        """)

    # Display conversation
    for message in st.session_state.conversation:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Chariklo:** {message['content']}")

    # User input
    if user_input := st.chat_input("What's present for you right now?"):
        st.session_state.pending_user_input = user_input
        st.rerun()

    # Process pending input
    if "pending_user_input" in st.session_state:
        user_input = st.session_state.pending_user_input
        del st.session_state.pending_user_input
        
        # Add user message
        if not (st.session_state.conversation and 
                st.session_state.conversation[-1]["role"] == "user" and 
                st.session_state.conversation[-1]["content"] == user_input):
            st.session_state.conversation.append({"role": "user", "content": user_input})
            
            # Get Chariklo response
            try:
                response = get_chariklo_response(user_input, st.session_state.memory_system)
                st.session_state.conversation.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error getting response: {e}")
                
        st.rerun()

    # Mark important button
    if st.session_state.conversation and len(st.session_state.conversation) >= 2:
        if st.button("⭐ Mark this moment as important", key="mark_important"):
            # Add last exchange to memory
            last_user = None
            last_assistant = None
            
            for msg in reversed(st.session_state.conversation):
                if msg["role"] == "assistant" and not last_assistant:
                    last_assistant = msg["content"]
                elif msg["role"] == "user" and not last_user:
                    last_user = msg["content"]
                    
                if last_user and last_assistant:
                    break
                    
            if last_user and last_assistant:
                conversation_snippet = f"User: {last_user}\nChariklo: {last_assistant}"
                st.session_state.memory_system.mark_memory(
                    conversation_snippet, "User marked as important"
                )
                st.success("✨ Moment saved to memory")
                
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.error("Please ensure all dependencies are installed.")
    st.error("Try: pip install -r requirements.txt")
    
except Exception as e:
    st.error(f"Error loading Chariklo: {e}")
    st.error(f"Working directory: {os.getcwd()}")
    
    # Show debug info
    st.error("Python path:")
    for path in sys.path[:5]:  # Show first 5 paths
        st.text(f"  {path}")
        
    st.error("Available files:")
    try:
        files = os.listdir(".")
        st.text(f"  {files[:10]}")  # Show first 10 files
    except:
        st.text("  Could not list files")
    st.error(f"Python path: {sys.path[:3]}...")
    st.stop()
