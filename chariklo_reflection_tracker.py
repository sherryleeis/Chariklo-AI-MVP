# chariklo_reflection_tracker.py
"""
Tracks real-time authentic moments for Chariklo.
AI logs only when it recognizes its own authentic engagement (not by external metric).
"""
from datetime import datetime

class CharikloReflectionTracker:
    def __init__(self):
        self.reflection_log = []  # List of dicts: {moment, context, my_response, timestamp}

    def log_authentic_moment(self, user_input: str, my_response: str, internal_note: str):
        """AI calls this when it recognizes its own authentic engagement"""
        self.reflection_log.append({
            "moment": internal_note,  # e.g. "This surprised me because..."
            "context": user_input,
            "my_response": my_response,
            "timestamp": datetime.now()
        })

    def get_log(self):
        return self.reflection_log
