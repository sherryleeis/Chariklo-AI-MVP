from typing import Dict, List, Optional
import os
import anthropic
from dotenv import load_dotenv  
import re
import time
import logging
from chariklo.chariklo_loop_detection import CharikloLoopDetection

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize the Anthropic API client
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ✅ Debugging: Ensure API Key is Loaded
if not anthropic_client.api_key:
    raise ValueError("❌ ERROR: Anthropic API Key not found. Check your .env file!")

# ✅ Configure Logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("watchdog.observers.inotify_buffer").setLevel(logging.WARNING)

class CharikloCore:
    def __init__(self):
        self.loop_detector = CharikloLoopDetection()
        # Core State Patterns remain the same but ensure analysis matches debug view
        self.state_patterns = {
            "resistance": {
                "high": {
                    "patterns": [
                        r"this (won't|isn't going to) work|pointless|stupid",
                        r"waste of (time|energy)",
                        r"(can't|don't) see the point"
                    ],
                    "response_type": "minimal acknowledgment",
                    "timing": "immediate"
                },
                "medium": {
                    "patterns": [
                        r"don't (know|see|understand)|maybe|guess",
                        r"not sure (about|if) this",
                        r"skeptical|doubtful"
                    ],
                    "response_type": "space holding",
                    "timing": "standard"
                }
            },
    "engagement": {
        "notice_dismiss": {
            "patterns": [
                r"(I notice|noticed|felt|experienced|sensed) (something|a shift|a change).*?(but|probably|just|might be|maybe|not sure)",
                r"something.*?(happening|changing|shifting).*?(but|probably|maybe|not sure)",
                r"(interesting|different|odd|unusual).*?(but|however|though|maybe|not sure)"
            ],
            "response_type": "neutral acknowledgment",
            "timing": "extended"
        },
        "intellectual": {
            "patterns": [
                r"wonder if|logical|explanation|theory",
                r"trying to (understand|figure out)",
                r"analyze|examine|investigate"
            ],
            "response_type": "allow exploration",
            "timing": "user_paced"
        },
        "processing": {
            "patterns": [
                r"need (to think|time)",
                r"processing|integrating",
                r"letting that sink in"
            ],
            "response_type": "maintain silence",
            "timing": "extended"
        }
    },
    "engagement": {
        "notice_dismiss": {
            "patterns": [
                r"(I notice|noticed|felt|experienced|sensed) (something|a shift|a change).*?(but|probably|just|might be|maybe|not sure)",
                r"something.*?(happening|changing|shifting).*?(but|probably|maybe|not sure)",
                r"(interesting|different|odd|unusual).*?(but|however|though|maybe|not sure)"
            ],
            "response_type": "neutral acknowledgment",
            "timing": "extended"
        },
        "intellectual": {
            "patterns": [
                r"wonder if|logical|explanation|theory",
                r"trying to (understand|figure out)",
                r"analyze|examine|investigate"
            ],
            "response_type": "allow exploration",
            "timing": "user_paced"
        },
        "processing": {
            "patterns": [
                r"need (to think|time)",
                r"processing|integrating",
                r"letting that sink in"
            ],
            "response_type": "maintain silence",
            "timing": "extended"
        }
    },

"notice_dismiss": {
    "patterns": [
        r"(I notice|felt|noticed|experienced|sensed) (something|a shift|a change).*?(but|probably|just|might be|maybe|not sure)",
        r"something.*?(happening|changing|shifting).*?(but|probably|maybe|not sure)",
        r"(interesting|different|odd|unusual).*?(but|however|though|maybe|not sure)"
    ],
    "response_type": "neutral acknowledgment",
    "timing": "extended"
},

                "intellectual": {
                    "patterns": [
                        r"wonder if|logical|explanation|theory",
                        r"trying to (understand|figure out)",
                        r"analyze|examine|investigate"
                    ],
                    "response_type": "allow exploration",
                    "timing": "user_paced"
                },
                "processing": {
                    "patterns": [
                        r"need (to think|time)",
                        r"processing|integrating",
                        r"letting that sink in"
                    ],
                    "response_type": "maintain silence",
                    "timing": "extended"
                }
            }
        

        # Thought Pattern Recognition
        # Thought Pattern Recognition
        self.thought_patterns = {
            "rumination": {
                "patterns": [
                    r"(keep|always|constantly) thinking about",
                    r"can't stop (thinking|wondering|worrying)",
                    r"going (in circles|around and around)",
                    r"same thoughts? over and over"
                ],
                "response_type": "awareness_opening",
                "timing": "gentle_interrupt"
            },
            "emotional_fixation": {
                "patterns": [
                    r"(so|really|just) (angry|upset|frustrated)",
                    r"(can't|won't) (accept|handle|deal with)",
                    r"(keeps|always) happening"
                ],
                "response_type": "sensation_inquiry",
                "timing": "after_expression"
            },
            "cognitive_distortion": {
                "patterns": [
                    r"(never|always|everyone|nobody)",
                    r"(worst|terrible|awful|horrible)",
                    r"(must|should|have to)"
                ],
                "response_type": "presence_offering",
                "timing": "natural_pause"
            },
            "avoidance": {
                "patterns": [
                    r"(logically|rationally|objectively) speaking",
                    r"(analyze|understand|figure out)",
                    r"(shouldn't|doesn't) affect me"
                ],
                "response_type": "gentle_grounding",
                "timing": "after_rationalization"
            },
            "identification": {
                "patterns": [
                    r"(feels like me|I am this|this is me)",
                    r"(so strong|overwhelming).*?(feels like me)",
                    r"(this is who I am|this defines me)"
                ],
                "response_type": "core_redirection",
                "timing": "gentle_interrupt"
            }
        }  # ✅ Correct closing bracket for self.thought_patterns


        # Awareness Openings
        self.presence_offerings = {
            "awareness_opening": [
                "Would you like to sit with what's arising?",
                "Is there a sensation that stands out right now?",
                ""  # Pure presence
            ],
            "sensation_inquiry": [
                "Notice where this is sitting in your body.",
                "That can be felt.",
                ""  # Space for noticing
            ],
            "gentle_grounding": [
                "This can be noticed.",
                ""  # Allow natural awareness
                "That's seen."
            ]
        }
        # Core Redirections - Ensuring identity is not mistaken for sensation
        self.core_redirections = {
            "wholeness": "Nothing I say can fill a space that is already whole.",
            "presence": "The sensation is present, but it is not you.",
            "sufficiency": "This moment is already full. What more is needed?",
            "identification": "The sensation is present, but it is not you."
        }

        # Timing Control - ensuring compatibility with API retry logic
        self.timing_control = {
            "immediate": 1,
            "standard": 3,
            "extended": 5,
            "user_paced": None
        }

    def analyze_input(self, text: str) -> Dict:
        """Analyze user input and return analysis with response type"""
        state = {
            "resistance_level": self.detect_resistance(text),
            "engagement_type": self.detect_engagement(text),
            "thought_pattern": self.detect_thought_pattern(text),
            "timing": self.calculate_timing(text),
            "presence_quality": self.determine_presence_state(text),
        }

        # ✅ Ensure response_type is assigned!
        state["response_type"] = self.get_response_type(state)
        state["loop_type"] = self.loop_detector.detect_loop(text)  # ✅ Ensures loop_type is assigned
        thought_pattern = self.detect_thought_pattern(text)
        logging.debug(f"🛠️ Thought pattern detected in analyze_input: {thought_pattern}")
        logging.debug(f"🛠️ Analyzed Input: {text}")
        logging.debug(f"📊 Analysis Result: {state}")
        
        return state


    def call_anthropic_api(self, prompt: str) -> str:
        """Calls the Anthropic API and returns the response."""
        try:
            response = anthropic_client.completions.create(
                model="claude-2",  # Adjust to your model
                max_tokens=500,
                prompt=prompt
            )
            logging.debug(f"Anthropic API Response: {response}")
            return response.completion.strip()  # Extract the completion
        except Exception as e:
            logging.error(f"❌ API Call Failed: {e}")
            return "⚠️ Unable to process request."
    

    def detect_thought_pattern(self, text: str) -> str:
        """Detect repetitive cognitive loops."""
        for pattern_type, info in self.thought_patterns.items():
            if any(re.search(pattern, text, re.I) for pattern in info["patterns"]):
                logging.debug(f"🔍 Thought pattern detected: {pattern_type}")
                return pattern_type
        return "neutral"
    def detect_resistance(self, text: str) -> str:
        """Detect level of resistance in user input, but ignore when user is processing."""
        if self.detect_engagement(text) == "processing":
            return "none"  # ✅ Ignore resistance if processing is detected

        for level, info in self.state_patterns["resistance"].items():
            for pattern in info["patterns"]:
                if re.search(pattern, text, re.I):
                    logging.debug(f"🔍 Matched Resistance Pattern: {pattern}")
                    return level
        return "low"

    def detect_engagement(self, text: str) -> str:
        """Detect type of engagement in user input."""
        for type_, info in self.state_patterns["engagement"].items():
            for pattern in info["patterns"]:
                if re.search(pattern, text, re.I):
                    logging.debug(f"🔍 Matched Engagement Pattern: {pattern} → {type_}")
                    return type_
        logging.debug(f"❌ No engagement match found. Available types: {list(self.state_patterns['engagement'].keys())}")
        return "neutral"

    def determine_presence_state(self, text: str) -> str:
        """Determine presence quality based on engagement/resistance."""
        engagement = self.detect_engagement(text)
        resistance = self.detect_resistance(text)

        if resistance == "high":
            return "minimal"
        if engagement == "processing":
            return "spacious"
        return "neutral"

    def calculate_timing(self, text: str) -> str:
        """Determine timing of response based on detected patterns."""
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
    def generate_response(self, analysis: Dict) -> str:
        """Generate appropriate response based on analysis, ensuring redirections trigger correctly."""

        # 🔹 Detect thought loops first
        loop_response = self.loop_detector.get_loop_response(analysis["loop_type"])
        if loop_response:
            logging.debug(f"Loop detected, responding with: {loop_response}")
            return loop_response  # ✅ Prioritize loop handling

        # 🔹 Check for core redirections
        thought_pattern = analysis.get("thought_pattern", "neutral")
        logging.debug(f"Thought pattern detected: {thought_pattern}")

        if thought_pattern in self.core_redirections:
            logging.debug(f"Redirecting to core response: {self.core_redirections[thought_pattern]}")
            return self.core_redirections[thought_pattern]

        else:
            logging.debug("Core redirection NOT triggered.")

        # 🔹 Default response selection
        response_type = analysis.get("response_type", "neutral acknowledgment")
        logging.debug(f"No core redirection, using response type: {response_type}")
        return self.call_anthropic_api("The user input relates to: " + str(analysis))


    def get_response_type(self, analysis: Dict) -> str:
        """Determine appropriate response type based on analysis."""
        if analysis["thought_pattern"] in self.thought_patterns:
            return self.thought_patterns[analysis["thought_pattern"]]["response_type"]
        elif analysis["resistance_level"] == "high":
            return "minimal acknowledgment"
        elif analysis["engagement_type"] in self.state_patterns["engagement"]:
            return self.state_patterns["engagement"][analysis["engagement_type"]]["response_type"]
        return "neutral acknowledgment"
