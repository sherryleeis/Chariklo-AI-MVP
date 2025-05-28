# chariklo_awareness_layer.py
"""
Supplies soft-tone guidance to Chariklo based on resistance, engagement, stuckness, loops — but never controls her behavior.
This layer:
- Replaces hard routing logic
- Returns gentle awareness flags
- Lets Chariklo remain presence-based and non-directive
- Is safe to call from generate_chariklo_response without hijacking tone
"""

import re

class CharikloAwarenessLayer:
    def __init__(self):
        # Define soft pattern sets for awareness
        self.resistance_patterns = [
            r"pointless|won't work|waste of time|can't see the point|not sure|skeptical|doubtful"
        ]
        self.engagement_patterns = [
            r"let me try|I'm willing|I'm curious|I want to understand|I'm open|let's see"
        ]
        self.stuckness_patterns = [
            r"stuck|can't move|can't decide|trapped|in a loop|can't stop|always|never"
        ]
        self.loop_patterns = [
            r"keep thinking|going in circles|same thoughts|over and over|looping"
        ]

    def get_awareness_flags(self, user_input: str) -> dict:
        """
        Returns a dict of awareness flags (True/False) for resistance, engagement, stuckness, loops.
        """
        text = user_input.lower()
        return {
            "resistance": any(re.search(p, text) for p in self.resistance_patterns),
            "engagement": any(re.search(p, text) for p in self.engagement_patterns),
            "stuckness": any(re.search(p, text) for p in self.stuckness_patterns),
            "loop": any(re.search(p, text) for p in self.loop_patterns),
        }

    def summarize_flags(self, flags: dict) -> str:
        """
        Returns a gentle, presence-based summary string for logging or optional tone modulation.
        """
        hints = []
        if flags.get("resistance"):
            hints.append("(noticing resistance)")
        if flags.get("engagement"):
            hints.append("(engagement present)")
        if flags.get("stuckness"):
            hints.append("(stuckness detected)")
        if flags.get("loop"):
            hints.append("(possible looping)")
        if not hints:
            return "(neutral awareness)"
        return " ".join(hints)
