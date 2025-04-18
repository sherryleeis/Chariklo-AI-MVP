from typing import Dict, Optional
import os
import re
import json
import logging
from anthropic import Anthropic
from dotenv import load_dotenv
from chariklo_system_prompt import SYSTEM_PROMPT
from chariklo_loop_detection import CharikloLoopDetection
from chariklo_patterns import state_patterns, thought_patterns
from chariklo_tone import ToneFilter
from chariklo_stuckness import StucknessHandler

# Normalize text
def normalize_text(text):
    return re.sub(r"[^\w\s]", "", text.lower().strip())

# Logging Configuration
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.getLogger("anthropic").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
chariklo_logger = logging.getLogger("chariklo")
chariklo_logger.setLevel(getattr(logging, log_level, logging.INFO))

# Load Memory Bank
try:
    with open('chariklo_memory_bank.json', 'r') as f:
        memory_bank = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("❌ ERROR: Memory bank file 'chariklo_memory_bank.json' not found!")
except json.JSONDecodeError:
    raise ValueError("❌ ERROR: Memory bank file is not a valid JSON!")

# Load API Environment
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("❌ ERROR: Anthropic API Key not found. Check your .env file!")

model_name = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
if not model_name:
    raise ValueError("❌ ERROR: Claude model name not found. Check your .env file!")

# Initialize Claude Client
client = Anthropic(api_key=api_key)

class CharikloCore:
    def __init__(self):
        self.loop_detector = CharikloLoopDetection()
        self.state_patterns = state_patterns
        self.thought_patterns = thought_patterns
        self.tone_filter = ToneFilter()
        self.stuckness_handler = StucknessHandler()

    def detect_user_accepts_sound(self, user_input: str, sound_type: str = "bell") -> bool:
        patterns = {
            "bell": r"(bell|ring|okay|sure|yes|please|yes please|go ahead|let's do it|awesome)",
            "rain": r"(rain|ring|okay|sure|yes|please|yes please|go ahead|let's do it|awesome)",
            "ocean": r"(ocean|ring|okay|sure|yes|please|yes please|go ahead|let's do it|awesome)",
        }
        pattern = patterns.get(sound_type.lower())
        return bool(re.search(pattern, user_input.lower())) if pattern else False

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
        for memory in memory_bank:
            if normalize_text(memory.get("cue", "")) == normalize_text(analysis["raw_input"]):
                chariklo_logger.info(f"🔍 [Exact Cue Match] ID: {memory['id']}")
                return memory

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

    def call_anthropic_api(self, user_input: str) -> str:
        try:
            response = client.messages.create(
                model=model_name,
                max_tokens=500,
                system=SYSTEM_PROMPT,  # ✅ Set system prompt here
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            return ''.join(block.text for block in response.content).strip()

        except Exception as e:
            print("Claude API error:", e)
            return "⚠️ Claude could not complete this request."