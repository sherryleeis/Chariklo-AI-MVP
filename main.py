import streamlit as st
import sys
import os
from pathlib import Path

# Get the absolute path to the project root
project_root = Path(__file__).parent.absolute()

# Add project root to Python path for imports
sys.path.insert(0, str(project_root))

# Set page config first
st.set_page_config(
    page_title="Chariklo: AI for Inner Space",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import and run the main app
try:
    # Change working directory to project root for relative imports
    os.chdir(project_root)
    
    # Import the main app module
    exec(open(project_root / "app" / "streamlit_app.py").read())
    
except Exception as e:
    st.error(f"Error loading Chariklo: {e}")
    st.error("Please check that all dependencies are installed correctly.")
    st.error(f"Working directory: {os.getcwd()}")
    st.error(f"Python path: {sys.path[:3]}...")
    st.stop()
