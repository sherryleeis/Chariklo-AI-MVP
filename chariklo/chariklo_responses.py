# chariklo_responses.py
"""
Handles response generation for different cognitive and emotional states.
"""

import re

class CharikloResponses:
    def __init__(self):
        self.response_qualities = {
            "minimal acknowledgment": ["I hear you."],
            "neutral acknowledgment": ["Noted."],
            "allow exploration": ["Tell me more about that."],
            "maintain silence": [""],  # Silent response for deep processing
            "space holding": ["I'm here."],
            "awareness_opening": ["Would you like to sit with what's arising?"],
            "sensation_inquiry": ["Notice where this is sitting in your body."],
            "presence_offering": ["This can be noticed."],
            "gentle_grounding": ["This moment is already full. What more is needed?"]
        }

        self.core_redirections = {
            "wholeness": "Nothing I say can fill a space that is already whole.",
            "identification": "The sensation is present, but it is not you.",
            "sufficiency": "This moment is already full. What more is needed?"
        }

    def get_response(self, response_type: str) -> str:
        """Retrieve a response based on the determined response type."""
        return self.response_qualities.get(response_type, [""])[0]

    def check_core_redirection(self, thought_pattern: str) -> str:
        """Check if the user's input matches a core redirection pattern."""
        return self.core_redirections.get(thought_pattern, "")
