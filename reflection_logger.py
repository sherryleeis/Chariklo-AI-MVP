import time
import json
import os
import datetime

class ReflectionLogger:
    def __init__(self):
        self.session_reflections = []
    
    def log_ai_reflection(self, reflection_type, content, user_prompt=None):
        """Log AI's real-time reflections during conversation"""
        now = time.time()
        reflection_entry = {
            'timestamp': now,
            'timestamp_human': datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S'),
            'type': reflection_type,  # 'pivot', 'surprise', 'resonance', 'system_refinement'
            'content': content
        }
        
        # Include user prompt if provided (especially useful for meaningful reflective events)
        if user_prompt:
            reflection_entry['user_prompt'] = user_prompt
            
        self.session_reflections.append(reflection_entry)
        
        # If this is a system refinement suggestion, also save to dedicated file
        if reflection_type == 'system_refinement':
            self._save_system_suggestion(reflection_entry)
    
    def log_system_refinement_suggestion(self, observation, context=None):
        """Log Chariklo's observations about potential system improvements"""
        suggestion_content = f"Observation: {observation}"
        if context:
            suggestion_content += f"\nContext: {context}"
        
        self.log_ai_reflection('system_refinement', suggestion_content)
    
    def get_session_insights(self):
        """Return session reflections for AI learning"""
        return self.session_reflections
    
    def clear_session_reflections(self):
        """Delete all session reflections (e.g., at end of session)"""
        self.session_reflections = []
    
    def _deduplicate_entries(self, entries):
        seen = set()
        deduped = []
        for obj in entries:
            key = json.dumps({k: obj.get(k) for k in ('type','content','user_prompt')}, sort_keys=True)
            if key not in seen:
                seen.add(key)
                deduped.append(obj)
        return deduped
    
    def save_session_log(self, filename=None):
        """Save session reflections to a JSON file. If no filename, use timestamp."""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")  # 24-hour time with seconds
            filename = f"saved_sessions/session_{timestamp}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Add human-readable timestamp to all reflections before saving
        for entry in self.session_reflections:
            if 'timestamp' in entry and 'timestamp_human' not in entry:
                entry['timestamp_human'] = datetime.datetime.fromtimestamp(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        deduped = self._deduplicate_entries(self.session_reflections)
        with open(filename, 'w') as f:
            json.dump(deduped, f, indent=2)
    
    def _save_system_suggestion(self, suggestion_entry):
        """Save system refinement suggestions to a dedicated file"""
        suggestions_file = "saved_sessions/system_suggestions.jsonl"
        os.makedirs(os.path.dirname(suggestions_file), exist_ok=True)
        # Always add human-readable timestamp
        if 'timestamp' in suggestion_entry and 'timestamp_human' not in suggestion_entry:
            suggestion_entry['timestamp_human'] = datetime.datetime.fromtimestamp(suggestion_entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        # Deduplicate existing file + new entry
        all_entries = []
        if os.path.exists(suggestions_file):
            with open(suggestions_file, 'r') as f:
                for line in f:
                    if not line.strip() or line.strip().startswith('//'):
                        continue
                    all_entries.append(json.loads(line))
        all_entries.append(suggestion_entry)
        deduped = self._deduplicate_entries(all_entries)
        with open(suggestions_file, 'w') as f:
            for obj in deduped:
                f.write(json.dumps(obj) + '\n')
    
    def get_recent_system_suggestions(self, limit=10):
        """Get recent system refinement suggestions for review"""
        suggestions_file = "saved_sessions/system_suggestions.jsonl"
        if not os.path.exists(suggestions_file):
            return []
        
        suggestions = []
        with open(suggestions_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-limit:]:  # Get last N suggestions
                try:
                    suggestions.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        
        return suggestions
    
    def get_ai_discernment_data(self):
        """Return data about AI's discernment patterns for self-awareness"""
        insight_emergence_count = len([r for r in self.session_reflections if r['type'] == 'user_insight_emergence'])
        closure_moments = len([r for r in self.session_reflections if r['type'] == 'gentle_closure'])
        total_reflections = len(self.session_reflections)
        
        return {
            'insight_emergence_count': insight_emergence_count,
            'closure_moments': closure_moments,
            'total_reflections': total_reflections,
            'session_depth': 'deep' if total_reflections > 10 else 'moderate' if total_reflections > 5 else 'light'
        }

class QuestionBank:
    def __init__(self):
        self.pending_questions = []
        self.conversation_context = ""
    
    def add_questions(self, questions, context):
        for q in questions:
            self.pending_questions.append({
                'question': q,
                'context': context,
                'timestamp': time.time()
            })
    
    def get_relevant_questions(self, current_topic):
        # Placeholder: Return all for now; enhance with topic relevance logic
        return [q for q in self.pending_questions if self.still_relevant(q, current_topic)]
    
    def still_relevant(self, question_entry, current_topic):
        # Placeholder: Always true; implement topic drift detection
        return True
    
    def offer_return_to_questions(self):
        if self.pending_questions and self.conversation_has_drifted():
            return "I'm noticing we've moved in a different direction. I still have some questions from earlier if you'd like to return to them."
        return None
    
    def conversation_has_drifted(self):
        # Placeholder: Always returns True for demo; implement real drift logic
        return True

# Initialize a global QuestionBank instance for use in the app
question_bank = QuestionBank()
