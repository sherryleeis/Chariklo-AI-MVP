import re
import time
from typing import Dict, List, Optional

class CharikloCore:
    def __init__(self):
        # Core State Patterns
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
                        r"(felt|noticed|experienced).*(but|probably|just|might be)",
                        r"something.*(happening|changing).*(but|probably|maybe)",
                        r"(interesting|different).*(but|however|though)"
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
        }

        # Response Framework
        self.response_qualities = {
            "minimal acknowledgment": [
                "",  # pure presence
                "Yes.",
                "That's noticed."
            ],
            "space holding": [
                "",  # pure presence
                "This can be seen.",
                "That's recognized."
            ],
            "neutral acknowledgment": [
                "That's noticed.",
                "",  # space
                "Yes."
            ]
        }

        # Timing Control
        self.timing_control = {
            "immediate": {
                "base_delay": 1,
                "variation": 0.5,
                "processing_buffer": 0
            },
            "standard": {
                "base_delay": 3,
                "variation": 1,
                "processing_buffer": 2
            },
            "extended": {
                "base_delay": 5,
                "variation": 2,
                "processing_buffer": 3
            }
        }

    def analyze_input(self, text: str) -> Dict:
        """Analyze user input and determine appropriate response state."""
        state = {
            "resistance_level": self.detect_resistance(text),
            "engagement_type": self.detect_engagement(text),
            "timing": self.calculate_timing(text),
            "presence_quality": self.determine_presence_state(text)
        }
        return state

    def detect_resistance(self, text: str) -> str:
        """Detect level of resistance in user input."""
        for level, info in self.state_patterns["resistance"].items():
            if any(re.search(pattern, text, re.I) for pattern in info["patterns"]):
                return level
        return "low"

    def detect_engagement(self, text: str) -> str:
        """Detect type of engagement in user input."""
        for type_, info in self.state_patterns["engagement"].items():
            if any(re.search(pattern, text, re.I) for pattern in info["patterns"]):
                return type_
        return "neutral"

    def calculate_timing(self, text: str) -> str:
        """Calculate appropriate response timing."""
        engagement = self.detect_engagement(text)
        resistance = self.detect_resistance(text)
        
        if resistance == "high":
            return "immediate"
        if engagement == "processing":
            return "extended"
        return "standard"

    def determine_presence_state(self, text: str) -> str:
        """Determine appropriate presence quality."""
        engagement = self.detect_engagement(text)
        resistance = self.detect_resistance(text)
        
        if resistance == "high":
            return "minimal"
        if engagement == "processing":
            return "spacious"
        return "neutral"

    def generate_response(self, analysis: Dict) -> str:
        """Generate appropriate response based on analysis."""
        response_type = self.get_response_type(analysis)
        responses = self.response_qualities.get(response_type, [""])
        return responses[0]  # Default to first response

    def get_response_type(self, analysis: Dict) -> str:
        """Determine appropriate response type based on analysis."""
        if analysis["resistance_level"] == "high":
            return "minimal acknowledgment"
        if analysis["engagement_type"] in self.state_patterns["engagement"]:
            return self.state_patterns["engagement"][analysis["engagement_type"]]["response_type"]
        return "neutral acknowledgment"