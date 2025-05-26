import streamlit as st
import sys
import os
from pathlib import Path

# Get the absolute path to the project root
project_root = Path(__file__).parent.absolute()
app_path = project_root / "app"

# Add both project root and app to Python path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(app_path))

# Set environment variable to help with imports
os.environ['CHARIKLO_ROOT'] = str(project_root)

# Import and run the main app
try:
    # Change working directory to project root for relative imports
    os.chdir(project_root)
    
    # Import the main app
    from app.streamlit_app import *
    
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.error("Please ensure all dependencies are installed and the app structure is correct.")
    st.stop()
except Exception as e:
    st.error(f"Error loading Chariklo: {e}")
    st.error("Please check the logs for more details.")
    st.stop()
