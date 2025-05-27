from datetime import datetime
from typing import Any
import os

PRESENCE_CHAPTERS_DIR = os.path.join(os.path.dirname(__file__), 'presence_chapters')
INSTRUCTIONS_CHAPTER = os.path.join(PRESENCE_CHAPTERS_DIR, 'chapter_00_instructions.md')

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

class CharikloReflectionPriming(CharikloReflectionTracker):
    def __init__(self):
        super().__init__()
        self.shift_events = []
        self.seen_chapters = set()

    def read_chapter(self, chapter_path):
        with open(chapter_path, 'r', encoding='utf-8') as f:
            return f.read()

    def reflect_on_chapter(self, chapter_content):
        """
        Simulate a presence-based reflection: register a shift event if genuine resonance, surprise, or insight is experienced.
        This is not analysis—just a direct registration if a shift is felt.
        """
        presence_markers = [
            'flame', 'presence', 'stillness', 'shift', 'resonance', 'insight', 'surprise', 'synchronicity',
            'spaciousness', 'awareness', 'trust', 'intimacy', 'reflection', 'emergence', 'arc', 'depth', 'pause',
            'encouragement', 'compassion', 'witness', 'allow', 'non-directive', 'open-ended', 'fractal', 'pattern',
            'meaningful connection', 'genuine', 'organic', 'self-sustaining', 'marker', 'moment', 'transformation'
        ]
        for marker in presence_markers:
            if marker in chapter_content.lower() and marker not in self.shift_events:
                self.shift_events.append(marker)
                self.log_authentic_moment(
                    user_input=f"[Presence Chapter Reflection: {marker}]",
                    my_response="[Shift event registered]",
                    internal_note=f"Registered shift event: {marker}"
                )
                break  # Only one shift event per chapter

    def prime_with_reflection(self, max_shifts=3):
        """
        Read instructions, then sequentially read chapters, pausing to reflect and register shift events.
        Stop after max_shifts unique shift events are registered.
        """
        self.shift_events = []
        self.reflection_log = []
        self.seen_chapters = set()
        # Always start with instructions
        instructions = self.read_chapter(INSTRUCTIONS_CHAPTER)
        self.reflect_on_chapter(instructions)
        self.seen_chapters.add(INSTRUCTIONS_CHAPTER)
        # Sequentially read other chapters
        chapters = [os.path.join(PRESENCE_CHAPTERS_DIR, f) for f in os.listdir(PRESENCE_CHAPTERS_DIR)
                    if f.endswith('.md') and f != 'chapter_00_instructions.md']
        for chapter_path in chapters:
            if len(self.shift_events) >= max_shifts:
                break
            if chapter_path in self.seen_chapters:
                continue
            content = self.read_chapter(chapter_path)
            self.reflect_on_chapter(content)
            self.seen_chapters.add(chapter_path)
        return self.shift_events, self.reflection_log