# chariklo_core.py
# Simplified core: system prompt integration, simple LLM call, and audio command processing

import os
import openai
import re
from chariklo.chariklo_system_prompt import SYSTEM_PROMPT

# --- System Prompt ---
CHARIKLO_SYSTEM_PROMPT = SYSTEM_PROMPT  # Or paste your refined prompt here

def get_chariklo_response(user_input, conversation_history):
    """Simple LLM call with system prompt - no complex logic"""
    messages = [
        {"role": "system", "content": CHARIKLO_SYSTEM_PROMPT},
        *conversation_history,
        {"role": "user", "content": user_input}
    ]
    response = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4"),
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

def play_audio(audio_type):
    """Simple audio player for [[bell]], [[rain-30]], etc."""
    audio_files = {
        'bell': 'assets/Bell.m4a',
        'rain-30': 'assets/rain_30sec.mp3',
        'ocean-60': 'assets/ocean_60sec.mp3',
        'forest-30': 'assets/forest_30sec.mp3'
    }
    return audio_files.get(audio_type)

def process_audio_commands(response_text):
    """Parse [[bell]] and similar commands, trigger audio, and clean response text."""
    import streamlit as st
    pattern = r"\[\[(.*?)\]\]"
    matches = re.findall(pattern, response_text)
    clean_text = re.sub(pattern, '', response_text)
    for match in matches:
        audio_path = play_audio(match.strip())
        if audio_path:
            st.audio(audio_path)
    return clean_text.strip()

def get_response_type(self, analysis) -> str:
        """
        Temporarily bypass old pattern matching system.
        Return a basic response type based on reflection cues or presence tier.
        """
        presence = analysis.get("presence_quality", "neutral")

        if presence == "minimal":
            return "minimal acknowledgment"
        elif presence == "spacious":
            return "mirror + silence"
        elif presence == "neutral":
            return "open reflection"
        else:
            return "default reflection"