# chariklo_core.py
# Refactored for clarity, presence, and graceful flow

from typing import Dict, Optional
import os
from anthropic import Anthropic
from dotenv import load_dotenv  
import re  # for normalize_text in cue matching
from chariklo.chariklo_system_prompt import SYSTEM_PROMPT
import time
import random
import json
import logging

def normalize_text(text):
    return re.sub(r"[^\w\s]", "", text.lower().strip())


# ─── Logging Configuration ─────────────────────────────
# ─── Logging Configuration ─────────────────────────────
# Silence Claude SDK logs
logging.getLogger("anthropic").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

# Optional: Configure your own named logger
chariklo_logger = logging.getLogger("chariklo")
chariklo_logger.setLevel(logging.DEBUG)  # Set to DEBUG to see debug messages

# Chariklo Modules
from chariklo_loop_detection import CharikloLoopDetection
from chariklo_patterns import state_patterns, thought_patterns
from chariklo_tone import ToneFilter
from chariklo_stuckness import StucknessHandler

# Load API Environment
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("❌ ERROR: Anthropic API Key not found. Check your .env file!")

model_name = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")

# ✅ New Claude 3 client
client = Anthropic(api_key=api_key)


class CharikloCore:
    def __init__(self):
        self.loop_detector = CharikloLoopDetection()
        self.state_patterns = state_patterns
        self.thought_patterns = thought_patterns
        self.tone_filter = ToneFilter()
        self.stuckness_handler = StucknessHandler()

    def detect_user_accepts_sound(self, user_input: str, sound_type: str = "bell") -> bool:
        """Enhanced detection of user acceptance for sound offerings"""
        # Core affirmative words - avoid matching these in exit responses
        affirmatives = (
            r"\b(okay|ok|sure|yes|please|yeah|yep|good|alright|fine|"
            r"definitely|absolutely|right|mhm|mm|mhmm|k)\b"
        )
        
        # Sound-specific patterns
        affirmative_patterns = {
            "bell": affirmatives,
            "rain": f"(\brain\b|{affirmatives})",
            "ocean": f"(\bocean\b|{affirmatives})"
        }
        
        pattern = affirmative_patterns.get(sound_type.lower())
        if not pattern:
            return False
            
        # Clean and check the input
        user_input_clean = user_input.lower().strip()
        
        # Skip if this is an exit response containing thanks
        if "thank" in user_input_clean and any(word in user_input_clean for word in ["helped", "better", "helpful"]):
            return False
            
        # Check for affirmative response
        return bool(re.search(pattern, user_input_clean))

    def analyze_input(self, text: str) -> Dict:
        state = {
            "resistance_level": self.detect_resistance(text),
            "engagement_type": self.detect_engagement(text),
            "thought_pattern": self.detect_thought_pattern(text),
            "timing": self.calculate_timing(text),
            "presence_quality": self.determine_presence_state(text),
        }
        state["response_type"] = self.get_response_type(state)
        state["loop_type"] = self.loop_detector.detect_loop(text)
        state["raw_input"] = text

        logging.debug(f"📊 Analysis Result: {state}")
        return state

    def detect_resistance(self, text: str) -> str:
        # Patterns have been deprecated; always return 'none' for now
        return "none"

    def detect_engagement(self, text: str) -> str:
        # Patterns have been deprecated; always return 'neutral' for now
        return "neutral"

    def detect_thought_pattern(self, text: str) -> str:
        # Patterns have been deprecated; always return 'neutral' for now
        return "neutral"

    def determine_presence_state(self, text: str) -> str:
        engagement = self.detect_engagement(text)
        resistance = self.detect_resistance(text)
        if resistance == "high":
            return "minimal"
        if engagement == "processing":
            return "spacious"
        return "neutral"

    def calculate_timing(self, text: str) -> str:
        pattern_type = self.detect_thought_pattern(text)
        resistance = self.detect_resistance(text)
        engagement = self.detect_engagement(text)

        if pattern_type in self.thought_patterns:
            return self.thought_patterns[pattern_type]["timing"]
        if resistance == "high":
            return "immediate"
        if engagement == "processing":
            return "extended"
        return "standard"

    def get_response_type(self, analysis: Dict) -> str:
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

    def generate_response(self, analysis: Dict) -> str:
        logging.debug(f"\U0001F9E0 Full analysis input: {analysis}")

        # 1. Loop response check
        loop_response = self.loop_detector.get_loop_response(analysis["loop_type"])
        if loop_response:
            return loop_response

        # 2. Stuckness handler (if present)
        thought_pattern = analysis.get("thought_pattern", "neutral")
        if hasattr(self.stuckness_handler, 'tiers') and thought_pattern in self.stuckness_handler.tiers:
            stuck_response = self.stuckness_handler.get_stuckness_response(thought_pattern, analysis)
            if stuck_response:
                return self.tone_filter.apply(stuck_response + " [stuckness]")

        # 3. Final fallback: LLM response
        raw_response = self.call_anthropic_api(analysis["raw_input"])
        response = self.tone_filter.apply(raw_response)

        # Presence-based bell trigger: if response_type is 'mirror + silence', append [[bell]]
        if analysis.get("response_type") == "mirror + silence":
            response = f"{response} [[bell]]"
        return response

    def get_bell_path(self) -> str:
        """Get the path to the bell sound file"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bell_path = os.path.join(base_dir, "Bell.m4a")
        if os.path.exists(bell_path):
            return bell_path
        else:
            chariklo_logger.error("❌ Bell sound file not found at: %s", bell_path)
            return None

    def call_anthropic_api(self, user_input: str) -> str:
        try:
            # Shortened system prompt logging - just first few lines
            chariklo_logger.info("🤖 System Prompt Preview:")
            first_lines = SYSTEM_PROMPT.split('\n')[:5]
            chariklo_logger.info("\n".join(first_lines) + "\n...")
            
            response = client.messages.create(
                model=model_name,
                max_tokens=500,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            response_text = ''.join(block.text for block in response.content).strip()
            chariklo_logger.info(f"🤖 Claude response: {response_text}")
            return response_text

        except Exception as e:
            chariklo_logger.error(f"❌ Claude API error: {e}")
            return "⚠️ Claude could not complete this request."