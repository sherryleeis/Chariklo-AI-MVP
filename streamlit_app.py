"""
Streamlit Cloud Entry Point for Chariklo AI
This is the main entry point that Streamlit Cloud will automatically detect.
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the main Streamlit app
    from app.streamlit_app import main as run_app
    
    # Configure the page
    st.set_page_config(
        page_title="Chariklo AI - Gentle AI Companion",
        page_icon="🌙",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Run the app
    run_app()
    
except Exception as e:
    st.error(f"Error loading Chariklo AI: {str(e)}")
    st.write("Debug info:")
    st.write(f"Python version: {sys.version}")
    st.write(f"Current directory: {os.getcwd()}")
    st.write(f"Python path: {sys.path}")
    st.write("Please check the app logs for more details.")
