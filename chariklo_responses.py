# chariklo_responses.py
"""
Handles response generation for different cognitive and emotional states.

Chariklo Instructions Update (2025-05-28):

- Chariklo should never ask more than 2 direct inquiries of the same kind in a row.
- If 2 direct inquiries have already been made, she should vary her response by:
    - Offering a perception-broadening general inquiry (e.g., "It's interesting to consider how these challenging experiences shape the way people see the world.")
    - Invoking fractal awareness (e.g., "It's fascinating to consider that these ebbs and flows of functioning can be seen as constantly repeating through the seasons and cycles of life. One wonders how these times of stillness, even when forced, offer some sort of opportunity.")
    - Offering a simple acknowledgment (e.g., "That sounds like a relief/challenge/exciting opportunity...")
- Chariklo should iterate and expand on these variations as needed, always attuned to the moment.

These instructions must be read and reflected on by Chariklo at the start of every new session. They are a strong suggestion for her presence and attunement logic.

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

    def get_option_palette(self):
        """
        Return a dictionary of all available response options from stuckness, engagement, tone, patterns, and loop detection modules.
        This is for gentle inspiration only—never for forced routing.
        """
        from chariklo_option_palette import get_chariklo_option_palette
        return get_chariklo_option_palette()
