import time

class UserControlledMemory:
    def __init__(self):
        self.session_memory = []
        self.marked_memories = []  # User-selected important moments
        self.memory_enabled = False
    
    def toggle_memory(self, enabled):
        """User controls whether AI remembers conversations"""
        self.memory_enabled = enabled
    
    def mark_memory(self, conversation_snippet, user_note=""):
        """User marks important moments to remember"""
        if self.memory_enabled:
            self.marked_memories.append({
                'content': conversation_snippet,
                'note': user_note,
                'timestamp': time.time()
            })
