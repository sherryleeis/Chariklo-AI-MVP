import time

class ReflectionLogger:
    def __init__(self):
        self.session_reflections = []
    
    def log_ai_reflection(self, reflection_type, content):
        """Log AI's real-time reflections during conversation"""
        self.session_reflections.append({
            'timestamp': time.time(),
            'type': reflection_type,  # 'pivot', 'surprise', 'resonance'
            'content': content
        })
    
    def get_session_insights(self):
        """Return session reflections for AI learning"""
        return self.session_reflections
    
    def clear_session_reflections(self):
        """Delete all session reflections (e.g., at end of session)"""
        self.session_reflections = []
