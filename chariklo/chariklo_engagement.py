# chariklo_engagement.py
"""
Handles engagement type detection based on user input.
"""
import re

class CharikloEngagement:
    def __init__(self):
        self.state_patterns = {
            "resistance": {
                "high": {"patterns": [r"this (won't|isn't going to) work", r"pointless", r"waste of time"],
                          "response_type": "minimal acknowledgment"},
                "medium": {"patterns": [r"not sure", r"skeptical", r"doubtful"],
                            "response_type": "space holding"}
            },
            "engagement": {
                "notice_dismiss": {"patterns": [r"felt.*but", r"interesting.*but"],
                                    "response_type": "neutral acknowledgment"},
                "intellectual": {"patterns": [r"wonder if", r"trying to understand"],
                                 "response_type": "allow exploration"},
                "processing": {"patterns": [r"processing", r"integrating"],
                               "response_type": "maintain silence"}
            }
        }
    
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
