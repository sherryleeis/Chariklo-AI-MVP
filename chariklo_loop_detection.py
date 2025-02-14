import re

class CharikloLoopDetection:
    def __init__(self):
        self.validation_patterns = {
            "repeated_seeking": {
                "markers": [
                    r"asking (same|similar) question",
                    r"returning to need for affirmation",
                    r"inability to disengage despite (tiredness|exhaustion)",
                    r"keeps checking for reassurance"
                ],
                "response": "reflect rather than feed"
            }
        }

    def detect_loop(self, text: str) -> str:
        """Detect if the user is stuck in a thought loop (e.g., repeated seeking)."""
        for loop_type, data in self.validation_patterns.items():
            if any(re.search(pattern, text, re.I) for pattern in data["markers"]):
                return loop_type
        return "no_loop"

    def get_loop_response(self, loop_type: str) -> str:
        """Return the appropriate response for detected loops."""
        loop_responses = {
            "repeated_seeking": "You've asked this before. What are you noticing in yourself right now?",
            "no_loop": ""  # If no loop detected, return empty to maintain presence
        }
        return loop_responses.get(loop_type, "")
