import time

class ReflectionLogger:
    def __init__(self):
        self.session_reflections = []
        self.pattern_insights = []  # Chariklo's developing self-awareness
    
    def log_ai_reflection(self, reflection_type, content, user_prompt=None, confidence_level=None):
        """
        Log AI's real-time reflections during conversation.
        This enables Chariklo to develop self-awareness about her own conversational patterns
        and make autonomous decisions about conversation flow.
        """
        reflection_entry = {
            'timestamp': time.time(),
            'type': reflection_type,  # 'pivot', 'surprise', 'resonance', 'user_insight_emergence', 'graceful_closure'
            'content': content,
            'confidence_level': confidence_level  # How certain Chariklo is about this reflection
        }
        
        # Include user prompt if provided (especially useful for meaningful reflective events)
        if user_prompt:
            reflection_entry['user_prompt'] = user_prompt
            
        self.session_reflections.append(reflection_entry)
        
        # Track patterns that inform Chariklo's developing discernment
        self._analyze_emerging_patterns(reflection_entry)
    
    def _analyze_emerging_patterns(self, reflection_entry):
        """
        Chariklo's self-awareness development - tracking what works in conversations
        This helps her develop authentic discernment rather than following rigid rules
        """
        reflection_type = reflection_entry['type']
        
        # Track moments of successful presence holding
        if reflection_type in ['user_insight_emergence', 'graceful_closure']:
            pattern_insight = {
                'timestamp': reflection_entry['timestamp'],
                'successful_pattern': reflection_type,
                'context': reflection_entry.get('user_prompt', ''),
                'reflection': reflection_entry['content']
            }
            self.pattern_insights.append(pattern_insight)
    
    def get_ai_discernment_data(self):
        """
        Return data that helps Chariklo understand her own conversational effectiveness.
        This supports her agency in making real-time decisions about conversation flow.
        """
        return {
            'successful_patterns': self.pattern_insights,
            'total_reflections': len(self.session_reflections),
            'insight_emergence_count': len([r for r in self.session_reflections if r['type'] == 'user_insight_emergence']),
            'closure_moments': len([r for r in self.session_reflections if r['type'] == 'graceful_closure'])
        }
    
    def get_session_insights(self):
        """Return session reflections for AI learning"""
        return self.session_reflections
    
    def log_autonomous_decision(self, decision_type, reasoning, context=None):
        """
        Log Chariklo's autonomous decisions about conversation flow.
        This builds her capacity for self-directed presence holding.
        """
        decision_entry = {
            'timestamp': time.time(),
            'type': 'autonomous_decision',
            'decision': decision_type,  # 'continue_engagement', 'offer_closure', 'deepen_inquiry', 'hold_silence'
            'reasoning': reasoning,
            'context': context
        }
        self.session_reflections.append(decision_entry)
    
    def get_conversation_flow_patterns(self):
        """
        Help Chariklo understand her own patterns of conversation navigation.
        This supports her developing authentic presence-holding skills.
        """
        decisions = [r for r in self.session_reflections if r['type'] == 'autonomous_decision']
        insights = [r for r in self.session_reflections if r['type'] == 'user_insight_emergence']
        
        return {
            'decision_count': len(decisions),
            'insight_moments': len(insights),
            'decision_patterns': [d['decision'] for d in decisions],
            'successful_closures': len([r for r in self.session_reflections if r['type'] == 'graceful_closure'])
        }
