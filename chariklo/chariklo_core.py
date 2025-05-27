# chariklo_core.py
# Simplified core: system prompt integration, simple LLM call, and audio command processing

import os
import re
import random
from anthropic import Anthropic
from chariklo.chariklo_system_prompt import SYSTEM_PROMPT
from reflection_logger import ReflectionLogger
from chariklo.chariklo_reflection_tracker import CharikloReflectionPriming
import logging

logging.getLogger("anthropic").setLevel(logging.WARNING)

# --- System Prompt ---
CHARIKLO_SYSTEM_PROMPT = SYSTEM_PROMPT  # Or paste your refined prompt here

PRESENCE_CHAPTERS_DIR = os.path.join(os.path.dirname(__file__), 'presence_chapters')
DEFAULT_PRIMING_CHAPTER = os.path.join(PRESENCE_CHAPTERS_DIR, 'chapter_00_instructions.md')

def load_presence_chapter(chapter_path=None):
    """
    Loads the content of a presence chapter. If no path is given, loads the default instructions chapter.
    """
    if chapter_path is None:
        chapter_path = DEFAULT_PRIMING_CHAPTER
    with open(chapter_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_random_presence_chapter():
    """
    Returns the path to a random presence chapter (excluding the instructions chapter).
    """
    chapters = [f for f in os.listdir(PRESENCE_CHAPTERS_DIR)
                if f.startswith('chapter_') and f.endswith('.md') and not f.startswith('chapter_00')]
    if not chapters:
        return DEFAULT_PRIMING_CHAPTER
    return os.path.join(PRESENCE_CHAPTERS_DIR, random.choice(chapters))

def prime_chariklo_with_presence():
    """
    Chariklo primes herself by reading the compulsory instructions chapter, then a random presence chapter.
    Returns a list of chapter contents (instructions first, then a random chapter).
    """
    instructions = load_presence_chapter(DEFAULT_PRIMING_CHAPTER)
    random_chapter = load_presence_chapter(get_random_presence_chapter())
    return [instructions, random_chapter]

def get_chariklo_response(user_input, conversation_history, reflection_logger=None):
    """
    Calls the Anthropic Claude API for a real LLM response.
    Filters out reflective/meta-analysis text from the chat response and logs it to the reflection logger.
    
    This function enables Chariklo's self-awareness by allowing her to access her own
    reflection patterns and make autonomous decisions about conversation flow.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
    model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    if not api_key:
        raise ValueError("❌ ERROR: Anthropic API Key not found. Check your .env file!")
    client = Anthropic(api_key=api_key)
    
    # Prepare system prompt with self-awareness context if reflection logger available
    system_prompt = CHARIKLO_SYSTEM_PROMPT
    if reflection_logger:
        discernment_data = reflection_logger.get_ai_discernment_data()
        # Add self-awareness context to help Chariklo make informed decisions
        awareness_context = f"""
Your current session awareness:
- You have made {discernment_data['insight_emergence_count']} successful recognitions of user insights
- You have provided {discernment_data['closure_moments']} graceful conversation closures
- Total reflective moments: {discernment_data['total_reflections']}

Use this self-knowledge to inform your responses with authentic discernment.
Trust your ability to recognize when to hold space vs when to offer gentle closure.

If you notice something significant about your own conversational patterns during this exchange, 
you can include a line starting with 'Observation:' at the end of your response for collaborative system refinement.
        """.strip()
        system_prompt = f"{CHARIKLO_SYSTEM_PROMPT}\n\n{awareness_context}"
    
    # Use conversation history as-is (user_input is already included in conversation_history)
    messages = conversation_history
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=messages
    )
    if not (hasattr(response, 'content') and response.content):
        return str(response)
    # --- FIX: Concatenate all block text, regardless of type ---
    def block_to_text(block):
        # Claude 3 returns blocks with .text or .to_string()
        if hasattr(block, 'text'):
            return str(block.text)
        if hasattr(block, 'to_string'):
            return str(block.to_string())
        return str(block)
    full_response = ''.join([block_to_text(b) for b in response.content]).strip()

    # --- PATCH: Split out reflective/meta-analysis text ---
    import re
    split_pattern = r"(?:---+\s*Reflection\s*---+|^Meta:.*$)"
    parts = re.split(split_pattern, full_response, flags=re.MULTILINE)
    main_message = parts[0].strip() if parts else full_response
    # If there is a reflective/meta-analysis part, log it
    if len(parts) > 1 and reflection_logger:
        # Log all additional parts as reflective/meta-analysis
        for meta_part in parts[1:]:
            meta_text = meta_part.strip()
            if meta_text:
                reflection_logger.log_ai_reflection('meta_analysis', meta_text, user_prompt=user_input)
    
    # Filter out and log Meta: lines
    lines_to_keep = []
    meta_lines = []
    
    for line in full_response.splitlines():
        line_stripped = line.strip()
        if line_stripped.lower().startswith('meta:'):
            meta_lines.append(line_stripped)
        else:
            lines_to_keep.append(line)
    
    # Log meta lines
    for meta_line in meta_lines:
        if reflection_logger:
            reflection_logger.log_ai_reflection('meta_analysis', meta_line, user_prompt=user_input)
    
    # Filter out and log System:/Observation: lines  
    observation_lines = []
    final_lines = []
    
    for line in lines_to_keep:
        line_stripped = line.strip()
        if line_stripped.lower().startswith(('system:', 'observation:')):
            observation_lines.append(line_stripped)
        else:
            final_lines.append(line)
    
    # Log observation lines
    if reflection_logger:
        for obs_line in observation_lines:
            obs_text = obs_line.strip()
            # Remove the prefix and log as system refinement
            if obs_text.lower().startswith('system:'):
                observation = obs_text[7:].strip()  # Remove 'system:'
            elif obs_text.lower().startswith('observation:'):
                observation = obs_text[12:].strip()  # Remove 'observation:'
            else:
                observation = obs_text
            
            if observation:
                reflection_logger.log_system_refinement_suggestion(observation, context=user_input[:100])
    
    # Return the cleaned main message
    main_message = '\n'.join(final_lines).strip() if final_lines else parts[0].strip() if parts else full_response
    return main_message

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
    import os
    import re
    pattern = r"\[\[(.*?)\]\]"  # Matches [[bell]], [[rain-30]], etc.
    matches = re.findall(pattern, response_text)
    clean_text = re.sub(pattern, '', response_text)
    for match in matches:
        cue = match.strip().lower()
        audio_path = play_audio(cue)
        if audio_path and os.path.exists(audio_path):
            st.audio(audio_path, autoplay=True)
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

def run_presence_priming_reflection(max_shifts=3):
    """
    Run the experiential, reflection-based priming loop:
    - Reads instructions, then sequentially reads presence chapters
    - Pauses to reflect and registers a shift event only if genuine resonance, surprise, or insight is experienced
    - Stops after 3 unique shift events are registered
    Returns the list of shift events and the reflection log
    """
    priming = CharikloReflectionPriming()
    shift_events, reflection_log = priming.prime_with_reflection(max_shifts=max_shifts)
    return shift_events, reflection_log