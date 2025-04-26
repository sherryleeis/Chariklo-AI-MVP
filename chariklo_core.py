# chariklo_core.py
# Refactored for clarity, presence, and graceful flow

from typing import Dict, Optional
import os
from anthropic import Anthropic
from dotenv import load_dotenv  
import re  # for normalize_text in cue matching
from chariklo_system_prompt import SYSTEM_PROMPT
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

# Load Memory Bank
with open('chariklo_memory_bank.json', 'r') as f:
    memory_bank = json.load(f)

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

    def detect_match(self, input_text: str, memory_fragment: dict) -> bool:
        """Enhanced semantic matching with prioritized exit handling"""
        input_clean = input_text.lower().strip()
        input_tokens = set(input_clean.split())
        
        # Get all possible cues from the memory fragment
        cues = memory_fragment.get('cues', [memory_fragment.get('cue', '')])
        if isinstance(cues, str):
            cues = [cues]

        # Positive indicators for exit/completion
        positive_indicators = {
            'better', 'clearer', 'helped', 'helpful', 'sense', 
            'good', 'thank', 'thanks', 'lighter', 'calmer',
            'understand', 'clear', 'clarity', 'peace', 'peaceful'
        }

        # 1. Check for exit-handling priority match
        if memory_fragment.get('id') == 'exit-gratitude-anchor-01':
            # Match on any positive indicator
            if any(word in input_tokens for word in positive_indicators):
                return True

        # 2. Check exact matches
        if any(cue.lower().strip() == input_clean for cue in cues):
            return True

        # 3. Check semantic similarity
        for cue in cues:
            cue_tokens = set(cue.lower().split())
            
            # Match if we share meaningful words
            if len(input_tokens.intersection(cue_tokens)) >= 2:
                # But only if not a negative context
                negative_indicators = {'not', 'dont', "don't", 'no', 'never'}
                if not input_tokens.intersection(negative_indicators):
                    return True

        # No match found after trying all strategies
        return False

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
        if self.detect_engagement(text) == "processing":
            return "none"
        for level, info in self.state_patterns["resistance"].items():
            if any(re.search(p, text, re.I) for p in info["patterns"]):
                return level
        return "low"

    def detect_engagement(self, text: str) -> str:
        for type_, info in self.state_patterns["engagement"].items():
            if any(re.search(p, text, re.I) for p in info["patterns"]):
                return type_
        return "neutral"

    def detect_thought_pattern(self, text: str) -> str:
        for pattern_type, info in self.thought_patterns.items():
            if any(re.search(p, text, re.I) for p in info["patterns"]):
                return pattern_type
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
        if analysis["thought_pattern"] in self.thought_patterns:
            return self.thought_patterns[analysis["thought_pattern"]]["response_type"]
        if analysis["resistance_level"] == "high":
            return "minimal acknowledgment"
        if analysis["engagement_type"] in self.state_patterns["engagement"]:
            return self.state_patterns["engagement"][analysis["engagement_type"]]["response_type"]
        return "neutral acknowledgment"

    def get_memory_match(self, analysis: Dict) -> Optional[dict]:
        # Always check for final exit after bell acceptance
        if analysis.get("bell_offered"):
            # If user responds after bell with thanks/affirmative
            if (self.detect_user_accepts_sound(analysis["raw_input"], "bell") or 
                any(word in analysis["raw_input"].lower() for word in ["thank", "bye", "goodbye"])):
                exit_final = next(
                    (memory for memory in memory_bank 
                    if memory.get('id') == 'final-exit-01'),
                    None
                )
                if exit_final:
                    chariklo_logger.info(f"🔍 [Final Exit] ID: {exit_final['id']}")
                    return exit_final
                return None  # Force silence if no final-exit found

        # Then check for initial exit patterns
        # But only if bell hasn't been offered yet AND isn't a bell response
        if not analysis.get("bell_offered") and not self.detect_user_accepts_sound(analysis["raw_input"], "bell"):
            exit_memory = next(
                (memory for memory in memory_bank 
                if memory.get('id') == 'exit-gratitude-anchor-01' 
                and self.detect_match(analysis["raw_input"], memory)),
                None
            )
            if exit_memory:
                chariklo_logger.info(f"🔍 [Exit Pattern Match] ID: {exit_memory['id']}")
                return exit_memory

        # Regular matching only if not in exit sequence
        if not analysis.get("bell_offered"):
            for memory in memory_bank:
                if self.detect_match(analysis["raw_input"], memory):
                    chariklo_logger.info(f"🔍 [Exact Cue Match] ID: {memory['id']}")
                    return memory

            # Fallback matching
            matches = []
            for memory in memory_bank:
                if (
                    memory["response_type"] == analysis["response_type"]
                    or memory.get("tier") == analysis["resistance_level"]
                    or memory.get("tier") == analysis["thought_pattern"]
                ):
                    matches.append(memory)
            if matches:
                chosen = random.choice(matches)
                chariklo_logger.info(f"🔍 [Fallback Match] ID: {chosen['id']}")
                return chosen

        return None

    def generate_response(self, analysis: Dict) -> str:
        logging.debug(f"🧠 Full analysis input: {analysis}")

        # 1. Loop response check
        loop_response = self.loop_detector.get_loop_response(analysis["loop_type"])
        if loop_response:
            return loop_response

        # 2. Presence memory match
        chariklo_logger.info(f"🧪 Raw user input: {analysis['raw_input']}")
        memory = self.get_memory_match(analysis)
        if memory:
            analysis["follows_with_silence"] = memory.get("follows_with_silence", False)
            analysis["offers_bell"] = memory.get("offers_bell", False)
            print("🪵 FOLLOW-UP: Silence is", analysis["follows_with_silence"])
            chariklo_logger.info(f"🔍 [Memory Match] Full Fragment: {json.dumps(memory, indent=2)}")
            print("🧘 CHARIKLO DEBUG — silence = True")
            return self.tone_filter.apply(memory["chariklo_response"])

        # 3. Core redirection check
        thought_pattern = analysis.get("thought_pattern", "neutral")
        if thought_pattern in self.stuckness_handler.tiers:
            stuck_response = self.stuckness_handler.get_stuckness_response(thought_pattern, analysis)
            if stuck_response:
                return self.tone_filter.apply(stuck_response + " [stuckness]")

        # 5. Final fallback: Soft edge-case support before Claude
        if "numb" in analysis["raw_input"].lower():
            logging.debug("🧪 Using soft fallback for 'numb' case.")
            return self.tone_filter.apply(
            "Even if it feels like nothing is happening, something brought you here. That’s worth noticing."
        )

        # 6. Absolute fallback: Claude
        raw_response = self.call_anthropic_api(analysis["raw_input"])
        return self.tone_filter.apply(raw_response)
    
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