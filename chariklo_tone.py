# chariklo_tone.py

class ToneFilter:
    """
    Applies final tone filtering to Chariklo's outgoing responses.
    Ensures all language is grounded, emotionally neutral, and non-performative.
    """

    def __init__(self):
        self.softened_terms = {
            "feel free to": "you may",
            "you might consider": "you could notice",
            "that’s okay": "",
            "you’ve got this": "",  # strip motivational phrases
            "breathe into it": "",  # strip overly spiritual phrases
            "let that go": "",      # too directive
        }

    def apply(self, text: str) -> str:
        for phrase, replacement in self.softened_terms.items():
            text = text.replace(phrase, replacement)
        return text.strip()
