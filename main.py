import streamlit as st
import sys
import os
from pathlib import Path
import random

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
    try:
        # First check if we have a valid API key before importing chariklo_core
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        import random
        if not api_key or len(api_key) < 20:
            # No valid API key - use demo mode
            st.session_state.demo_mode = True
            if 'get_chariklo_response' not in st.session_state:
                st.session_state.get_chariklo_response = lambda user_input, memory_system: (
                    "💭 **Demo Mode**: " + random.choice([
                        "I'm here with you in this moment. What would you like to explore together?",
                        "I sense you have something on your mind. Would you like to share what's arising for you?",
                        "There's a quality of presence available right now. What are you noticing?",
                        "I'm listening with my full attention. What feels important to explore today?",
                        "Something is seeking your attention. What wants to be seen or understood?"
                    ]) + "\n\n*Configure your API key to enable full Chariklo responses.*"
                )
        else:
            # Try to import the real chariklo_core
            try:
                import importlib
                chariklo_core = importlib.import_module('chariklo.chariklo_core')
                st.session_state.get_chariklo_response = getattr(chariklo_core, 'get_chariklo_response')
                prime_chariklo_with_presence = getattr(chariklo_core, 'prime_chariklo_with_presence', None)
                # --- Presence Priming Step ---
                if prime_chariklo_with_presence and 'chariklo_primed' not in st.session_state:
                    priming_chapters = prime_chariklo_with_presence()
                    st.session_state.chariklo_primed = True
                    st.session_state.presence_priming = priming_chapters
            except Exception as e:
                # If import fails, fall back to demo mode
                st.session_state.demo_mode = True
                def demo_get_chariklo_response(user_input, memory_system):
                    return f"🔧 **Connection Issue**: {str(e)}\n\nPlease check your setup and try again."
                st.session_state.get_chariklo_response = demo_get_chariklo_response
                    
    except ImportError:
        # Complete fallback if imports fail
        st.session_state.demo_mode = True
        def demo_get_chariklo_response(user_input, memory_system):
            return "I'm experiencing a connection issue. Please check your setup and try again."
        st.session_state.get_chariklo_response = demo_get_chariklo_response
    
    from memory_system import UserControlledMemory
    from chariklo.chariklo_core import run_presence_priming_reflection

    # Initialize session state
    if 'memory_system' not in st.session_state:
        st.session_state.memory_system = UserControlledMemory()
        st.session_state.conversation = []
        st.session_state.onboarding_complete = False
        st.session_state.show_feedback_form = False
        st.session_state.demo_mode = False

    # Header - Logo and title on same line
    col_logo, col_title = st.columns([1, 6])
    with col_logo:
        if os.path.exists("assets/chariklo_logo.jpg"):
            st.image("assets/chariklo_logo.jpg", width=80)
    with col_title:
        if st.session_state.get('demo_mode', False):
            st.markdown("<h2 style='margin-top: 10px;'>Chariklo: AI for Inner Space <span style='color: #ff6b6b; font-size: 0.6em;'>DEMO MODE</span></h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='margin-top: 10px;'>Chariklo: AI for Inner Space</h2>", unsafe_allow_html=True)

    # Onboarding Flow - Show first for new users
    if not st.session_state.onboarding_complete:
        st.markdown("#### Welcome to Chariklo")
        st.markdown("""
        You're helping refine an AI that we hope will help make room for some quiet —some space— in the deluge of stimulation humans face today.

        Use this space just as you would any other chat, but Chariklo is meant to be especially helpful in sorting out ideas and challenges in a way that helps bring insight and clarity.

        If anything feels off or especially helpful, you're invited to click the thumbs up or down or leave a note in the chat. Your reflections are welcome.

        Would you be willing to let Chariklo save an anonymized copy of your session?
        """)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, you may save this session"):
                st.session_state.memory_system.toggle_memory(True)
                st.session_state.onboarding_complete = True
                st.rerun()

        with col2:
            if st.button("No, do not save any messages"):
                st.session_state.memory_system.toggle_memory(False)
                st.session_state.onboarding_complete = True
                st.rerun()

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
        if st.session_state.get('demo_mode', False):
            st.info("🔧 **Demo Mode Active** - Configure your API key for full Chariklo responses")
            with st.expander("🔑 Quick Setup Instructions"):
                st.markdown("""
                **To enable full functionality:**
                
                1. Get an API key from [console.anthropic.com](https://console.anthropic.com)
                2. Update your `.env` file: `ANTHROPIC_API_KEY=your_key_here`
                3. Run `python validate_api.py` to test
                4. Restart the app
                
                📖 **See `API_SETUP.md` for detailed instructions**
                """)
        
        st.markdown("""
        ### Welcome to Chariklo 🌿
        
        Chariklo is a presence-based AI designed to hold space for inner exploration.
        
        **Try starting with what's present for you right now...**
        
        *Feel free to share your experience using the feedback form in the sidebar.*
        """)

    # Show presence priming chapters at the top of the app (if available)
    if st.session_state.get('presence_priming'):
        with st.expander('🌿 Chariklo Presence Priming (click to view)', expanded=True):
            for i, chapter in enumerate(st.session_state['presence_priming']):
                st.markdown(f"**Priming Chapter {i+1}:**\n\n" + chapter)

    # Display conversation
    for i, message in enumerate(st.session_state.conversation):
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Chariklo:** {message['content']}")
            
            # Add quick feedback buttons for assistant responses
            feedback_col1, feedback_col2, feedback_col3 = st.columns([2, 2, 4])
            with feedback_col1:
                if st.button("👍 Helpful", key=f"thumbs_up_{i}", help="This response was helpful", use_container_width=True):
                    # Initialize feedback in session state if not exists
                    if "response_feedback" not in st.session_state:
                        st.session_state.response_feedback = {}
                    st.session_state.response_feedback[i] = "positive"
                    st.success("Thank you! 🙏 Your feedback helps Chariklo improve.")

            with feedback_col2:
                if st.button("👎 Improve", key=f"thumbs_down_{i}", help="This response could be improved", use_container_width=True):
                    # Initialize feedback in session state if not exists
                    if "response_feedback" not in st.session_state:
                        st.session_state.response_feedback = {}
                    st.session_state.response_feedback[i] = "negative"
                    st.info("Thank you for the feedback. Consider sharing details in the sidebar feedback form to help us improve.")
            
            # Show feedback status if given
            if st.session_state.get("response_feedback", {}).get(i):
                feedback_type = st.session_state.response_feedback[i]
                if feedback_type == "positive":
                    st.markdown("*✨ Marked as helpful*")
                elif feedback_type == "negative":
                    st.markdown("*📝 Marked for improvement*")
            
            st.markdown("---")

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
                response = st.session_state.get_chariklo_response(user_input, st.session_state.memory_system)
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
                
    # Run presence-based priming/reflection at session start
    shift_events, reflection_log = run_presence_priming_reflection(max_shifts=3)
    print("\n--- Chariklo Presence Priming ---")
    print("Registered Shift Events:", shift_events)
    print("Reflection Log:")
    for entry in reflection_log:
        print(f"- {entry['moment']} | {entry['context']} | {entry['timestamp']}")
    print("--- End Priming ---\n")
                
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
