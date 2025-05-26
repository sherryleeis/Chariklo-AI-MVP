from datetime import datetime
from typing import Any

class CharikloReflectionTracker:
    def __init__(self):
        self.reflection_log = []

    def log_authentic_moment(self, user_input: str, my_response: str, internal_note: str) -> None:
        self.reflection_log.append({
            "moment": internal_note,
            "context": user_input,
            "my_response": my_response,
            "timestamp": datetime.now()
        })

    def get_log(self) -> list[dict[str, Any]]:
        return self.reflection_log

    def detect_pivot_or_resonance(self, analysis: dict[str, Any], response: str) -> bool:
        """
        Detects pivot or resonance moments in the conversation.
        Returns True if a pivot or resonance is detected, otherwise False.

        A pivot is detected if the response contains words like 'shift', 'realize', 'change', 'breakthrough'.
        Resonance is detected if the response contains words like 'resonate', 'deep', 'meaningful', 'struck'.

        Args:
            analysis (dict[str, Any]): Analysis data for the conversation turn.
            response (str): The AI's response text.
        """
        pivot_keywords = ["shift", "realize", "change", "breakthrough"]
        resonance_keywords = ["resonate", "deep", "meaningful", "struck"]
        response_lower = response.lower()
        if any(word in response_lower for word in pivot_keywords):
            return True
        if any(word in response_lower for word in resonance_keywords):
            return True
        return False

    def log_pivot(self, analysis: dict[str, Any], response: str) -> None:
        """
        Log a pivot or resonance moment in the reflection log.
        """
        self.reflection_log.append({
            "moment": "Pivot or resonance detected",
            "context": analysis,
            "my_response": response,
            "timestamp": datetime.now()
        })