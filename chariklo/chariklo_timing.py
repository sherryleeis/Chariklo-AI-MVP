# chariklo_timing.py
"""
Handles response timing based on user engagement and resistance.
"""
class CharikloTiming:
    def __init__(self):
        self.timing_control = {
            "immediate": 1,
            "standard": 3,
            "extended": 5,
            "user_paced": None
        }
    
    def get_timing(self, thought_pattern: str, resistance: str, engagement: str) -> str:
        """Determine timing for responses based on user state."""
        if resistance == "high":
            return "immediate"
        if engagement == "processing":
            return "extended"
        return self.timing_control.get(thought_pattern, "standard")
