"""
Contextual Behavior System for Chariklo

This module implements a flexible, context-aware system that determines appropriate
responses based on conversation flow, emotional context, and presence indicators
rather than rigid linguistic pattern matching.
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

class ContextualBehaviorAnalyzer:
    """
    Analyzes conversation context to determine appropriate behavioral responses
    without relying on hard-coded linguistic patterns.
    """
    
    def __init__(self):
        # Conversation flow states
        self.flow_indicators = {
            'opening': ['first', 'beginning', 'start', 'hello', 'hi'],
            'deepening': ['feel', 'sense', 'notice', 'aware', 'experiencing'],
            'processing': ['thinking', 'sitting with', 'letting', 'allowing'],
            'insight_emerging': ['realize', 'see', 'understand', 'clear', 'ah'],
            'completion': ['enough', 'complete', 'satisfied', 'thank you', 'ready'],
            'resistance': ['difficult', 'hard', 'struggle', 'can\'t', 'won\'t']
        }
        
        # Context patterns for presence detection
        self.presence_markers = {
            'high_presence': [
                'stillness', 'quiet', 'peaceful', 'centered', 'grounded',
                'spacious', 'open', 'aware', 'present'
            ],
            'emerging_presence': [
                'settling', 'slowing', 'breathing', 'noticing', 'feeling',
                'sensing', 'beginning to'
            ],
            'seeking_presence': [
                'need quiet', 'want peace', 'looking for', 'searching',
                'hoping to find', 'trying to'
            ],
            'presence_disrupted': [
                'distracted', 'scattered', 'anxious', 'restless', 'agitated',
                'overwhelmed', 'racing'
            ]
        }

    def analyze_conversation_context(self, conversation_history: List[Dict], 
                                  current_user_input: str) -> Dict:
        """
        Analyze the broader conversation context to determine appropriate response type.
        
        Returns a context analysis including:
        - conversation_phase: where we are in the flow
        - presence_level: user's current presence state
        - emotional_tone: general emotional context
        - pacing_needs: suggested response timing and length
        - sound_cue_appropriate: whether ambient sounds might help
        - soft_exit_opportunity: whether this is a natural closing point
        """
        
        # Analyze conversation flow
        conversation_phase = self._determine_conversation_phase(conversation_history, current_user_input)
        
        # Assess presence level
        presence_level = self._assess_presence_level(conversation_history, current_user_input)
        
        # Determine emotional context
        emotional_tone = self._analyze_emotional_tone(conversation_history, current_user_input)
        
        # Calculate pacing needs
        pacing_needs = self._calculate_pacing_needs(conversation_phase, presence_level, emotional_tone)
        
        # Check for sound cue appropriateness
        sound_cue_appropriate = self._should_offer_sound_cue(conversation_phase, presence_level)
        
        # Assess soft exit opportunity
        soft_exit_opportunity = self._assess_soft_exit_opportunity(conversation_history, current_user_input)
        
        return {
            'conversation_phase': conversation_phase,
            'presence_level': presence_level,
            'emotional_tone': emotional_tone,
            'pacing_needs': pacing_needs,
            'sound_cue_appropriate': sound_cue_appropriate,
            'soft_exit_opportunity': soft_exit_opportunity,
            'response_guidance': self._generate_response_guidance(
                conversation_phase, presence_level, emotional_tone
            )
        }

    def _determine_conversation_phase(self, conversation_history: List[Dict], 
                                    current_input: str) -> str:
        """Determine where we are in the conversation flow."""
        
        if len(conversation_history) <= 2:
            return 'opening'
        
        recent_messages = self._get_recent_messages(conversation_history, 3)
        combined_text = (current_input + ' ' + ' '.join(recent_messages)).lower()
        
        # Check for phase indicators
        phase_scores = {}
        for phase, indicators in self.flow_indicators.items():
            score = sum(1 for indicator in indicators if indicator in combined_text)
            phase_scores[phase] = score
        
        # If we have clear indicators, use those
        if max(phase_scores.values()) > 0:
            return max(phase_scores, key=phase_scores.get)
        
        # Otherwise, infer from conversation length and content
        total_exchanges = len([msg for msg in conversation_history if msg['role'] == 'user'])
        
        if total_exchanges <= 2:
            return 'opening'
        elif total_exchanges <= 5:
            return 'deepening'
        elif self._contains_contemplative_language(combined_text):
            return 'processing'
        else:
            return 'deepening'

    def _assess_presence_level(self, conversation_history: List[Dict], 
                             current_input: str) -> str:
        """Assess the user's current presence state."""
        
        recent_messages = self._get_recent_messages(conversation_history, 2)
        combined_text = (current_input + ' ' + ' '.join(recent_messages)).lower()
        
        # Score presence markers
        presence_scores = {}
        for level, markers in self.presence_markers.items():
            score = sum(1 for marker in markers if marker in combined_text)
            presence_scores[level] = score
        
        if max(presence_scores.values()) > 0:
            return max(presence_scores, key=presence_scores.get)
        
        # Infer from language patterns
        if self._contains_body_awareness(combined_text):
            return 'emerging_presence'
        elif self._contains_mental_activity(combined_text):
            return 'seeking_presence'
        else:
            return 'presence_disrupted'

    def _analyze_emotional_tone(self, conversation_history: List[Dict], 
                              current_input: str) -> str:
        """Analyze the emotional context."""
        
        recent_messages = self._get_recent_messages(conversation_history, 2)
        combined_text = (current_input + ' ' + ' '.join(recent_messages)).lower()
        
        # Emotional indicators
        if any(word in combined_text for word in ['calm', 'peaceful', 'settled', 'content']):
            return 'calm'
        elif any(word in combined_text for word in ['frustrated', 'angry', 'irritated', 'annoyed']):
            return 'agitated'
        elif any(word in combined_text for word in ['sad', 'grief', 'loss', 'heavy', 'hurt']):
            return 'grieving'
        elif any(word in combined_text for word in ['anxious', 'worried', 'nervous', 'scared']):
            return 'anxious'
        elif any(word in combined_text for word in ['curious', 'interested', 'wonder']):
            return 'curious'
        else:
            return 'neutral'

    def _calculate_pacing_needs(self, phase: str, presence_level: str, 
                              emotional_tone: str) -> Dict:
        """Calculate appropriate pacing for response."""
        
        base_pacing = {
            'response_length': 'medium',  # short, medium, long
            'pause_before': False,
            'pause_after': False,
            'silence_tolerance': 'medium'  # low, medium, high
        }
        
        # Adjust based on conversation phase
        if phase == 'opening':
            base_pacing['response_length'] = 'medium'
            base_pacing['silence_tolerance'] = 'low'
        elif phase == 'processing':
            base_pacing['response_length'] = 'short'
            base_pacing['pause_before'] = True
            base_pacing['silence_tolerance'] = 'high'
        elif phase == 'completion':
            base_pacing['response_length'] = 'short'
            base_pacing['pause_after'] = True
        
        # Adjust based on presence level
        if presence_level == 'high_presence':
            base_pacing['silence_tolerance'] = 'high'
            base_pacing['response_length'] = 'short'
        elif presence_level == 'presence_disrupted':
            base_pacing['silence_tolerance'] = 'low'
            base_pacing['response_length'] = 'medium'
        
        # Adjust based on emotional tone
        if emotional_tone == 'agitated':
            base_pacing['pause_before'] = True
            base_pacing['silence_tolerance'] = 'medium'
        elif emotional_tone == 'grieving':
            base_pacing['response_length'] = 'short'
            base_pacing['silence_tolerance'] = 'high'
        
        return base_pacing

    def _should_offer_sound_cue(self, phase: str, presence_level: str) -> bool:
        """Determine if ambient sound cues would be appropriate."""
        
        # Sound cues work well during processing phases with emerging presence
        if phase in ['processing', 'deepening'] and presence_level in ['emerging_presence', 'seeking_presence']:
            return True
        
        # Also appropriate during completion for settling
        if phase == 'completion' and presence_level != 'presence_disrupted':
            return True
        
        return False

    def _assess_soft_exit_opportunity(self, conversation_history: List[Dict], 
                                    current_input: str) -> bool:
        """Assess whether this is a natural conversation closing point."""
        
        # Look for completion indicators
        completion_indicators = [
            'thank you', 'thanks', 'appreciate', 'helpful', 'enough',
            'complete', 'satisfied', 'ready to go', 'that\'s all',
            'perfect', 'exactly what i needed'
        ]
        
        if any(indicator in current_input.lower() for indicator in completion_indicators):
            return True
        
        # Check conversation length - longer conversations may need gentle closing
        user_messages = [msg for msg in conversation_history if msg['role'] == 'user']
        if len(user_messages) > 8:  # After several exchanges
            return True
        
        # Look for settling language
        settling_language = ['feel better', 'clearer now', 'makes sense', 'settled']
        if any(phrase in current_input.lower() for phrase in settling_language):
            return True
        
        return False

    def _generate_response_guidance(self, phase: str, presence_level: str, 
                                  emotional_tone: str) -> Dict:
        """Generate specific guidance for crafting the response."""
        
        guidance = {
            'approach': 'neutral',  # minimal, neutral, exploratory, supportive
            'focus': 'presence',    # presence, sensation, awareness, integration
            'tone': 'calm',         # calm, gentle, spacious, grounding
            'avoid': []             # things to avoid in response
        }
        
        # Adjust approach based on phase
        if phase == 'opening':
            guidance['approach'] = 'supportive'
            guidance['focus'] = 'presence'
        elif phase == 'processing':
            guidance['approach'] = 'minimal'
            guidance['focus'] = 'awareness'
        elif phase == 'completion':
            guidance['approach'] = 'neutral'
            guidance['focus'] = 'integration'
        
        # Adjust based on presence level
        if presence_level == 'high_presence':
            guidance['approach'] = 'minimal'
            guidance['tone'] = 'spacious'
        elif presence_level == 'presence_disrupted':
            guidance['approach'] = 'supportive'
            guidance['focus'] = 'grounding'
            guidance['tone'] = 'gentle'
        
        # Adjust based on emotional tone
        if emotional_tone == 'agitated':
            guidance['avoid'] = ['advice', 'analysis', 'solutions']
            guidance['focus'] = 'sensation'
            guidance['tone'] = 'grounding'
        elif emotional_tone == 'grieving':
            guidance['approach'] = 'minimal'
            guidance['tone'] = 'gentle'
            guidance['avoid'] = ['fixing', 'positive reframing']
        
        return guidance

    def _get_recent_messages(self, conversation_history: List[Dict], count: int) -> List[str]:
        """Get the most recent user messages."""
        user_messages = [msg['content'] for msg in conversation_history 
                        if msg['role'] == 'user']
        return user_messages[-count:] if user_messages else []

    def _contains_contemplative_language(self, text: str) -> bool:
        """Check if text contains contemplative/processing language."""
        contemplative_words = [
            'sitting with', 'letting', 'allowing', 'noticing', 'observing',
            'feeling into', 'sensing', 'breathing with', 'holding'
        ]
        return any(phrase in text for phrase in contemplative_words)

    def _contains_body_awareness(self, text: str) -> bool:
        """Check if text contains body awareness language."""
        body_words = [
            'breath', 'breathing', 'heart', 'chest', 'belly', 'shoulders',
            'tension', 'relaxed', 'tight', 'warm', 'cool', 'sensation'
        ]
        return any(word in text for word in body_words)

    def _contains_mental_activity(self, text: str) -> bool:
        """Check if text indicates mental activity/seeking."""
        mental_words = [
            'thinking', 'thoughts', 'mind', 'wondering', 'trying to',
            'figure out', 'understand', 'confused', 'unclear'
        ]
        return any(word in text for word in mental_words)


class ContextualResponseGenerator:
    """
    Generates contextually appropriate responses based on behavior analysis.
    """
    
    def __init__(self):
        self.response_templates = {
            'minimal_acknowledgment': [
                "Mm.",
                "Yes.",
                "I'm here.",
                "..."
            ],
            'presence_invitation': [
                "What's here right now?",
                "Can you feel that?",
                "What do you notice?",
                "Let's stay with this."
            ],
            'grounding_support': [
                "Feel your feet on the ground.",
                "Can you sense your breath?",
                "What's solid beneath you?",
                "Notice what's supporting you."
            ],
            'spacious_holding': [
                "There's room for all of this.",
                "No need to change anything.",
                "Just let it be as it is.",
                "This too belongs."
            ],
            'gentle_closure': [
                "Take whatever time you need.",
                "This can settle in its own time.",
                "You can return to this whenever you're ready.",
                "There's no hurry."
            ]
        }

    def generate_contextual_response(self, context_analysis: Dict, 
                                   user_input: str) -> Dict:
        """
        Generate a response based on contextual analysis rather than pattern matching.
        """
        
        guidance = context_analysis['response_guidance']
        pacing = context_analysis['pacing_needs']
        
        # Determine response type based on context
        response_type = self._determine_response_type(context_analysis)
        
        # Generate response content
        response_content = self._craft_response_content(
            response_type, guidance, user_input
        )
        
        # Add any ambient cues if appropriate
        ambient_cues = []
        if context_analysis['sound_cue_appropriate']:
            ambient_cues = self._suggest_ambient_cues(context_analysis)
        
        # Determine if soft exit should be offered
        offer_soft_exit = context_analysis['soft_exit_opportunity']
        
        return {
            'response_content': response_content,
            'response_type': response_type,
            'pacing_guidance': pacing,
            'ambient_cues': ambient_cues,
            'offer_soft_exit': offer_soft_exit,
            'presence_focus': guidance['focus']
        }

    def _determine_response_type(self, context_analysis: Dict) -> str:
        """Determine the type of response needed."""
        
        phase = context_analysis['conversation_phase']
        presence = context_analysis['presence_level']
        approach = context_analysis['response_guidance']['approach']
        
        if approach == 'minimal':
            return 'minimal_acknowledgment'
        elif phase == 'processing' and presence in ['emerging_presence', 'high_presence']:
            return 'spacious_holding'
        elif presence == 'presence_disrupted':
            return 'grounding_support'
        elif phase == 'completion':
            return 'gentle_closure'
        else:
            return 'presence_invitation'

    def _craft_response_content(self, response_type: str, guidance: Dict, 
                              user_input: str) -> str:
        """Craft the actual response content."""
        
        # This would integrate with the main system prompt to generate
        # contextually appropriate responses rather than using templates
        base_templates = self.response_templates.get(response_type, 
                                                   self.response_templates['presence_invitation'])
        
        # Return guidance for the system prompt rather than a fixed response
        return {
            'type': response_type,
            'guidance': guidance,
            'focus_areas': self._identify_focus_areas(user_input),
            'avoid_patterns': guidance.get('avoid', [])
        }

    def _suggest_ambient_cues(self, context_analysis: Dict) -> List[str]:
        """Suggest appropriate ambient sound cues."""
        
        phase = context_analysis['conversation_phase']
        emotional_tone = context_analysis['emotional_tone']
        
        if phase == 'processing':
            if emotional_tone == 'agitated':
                return ['[[gentle ocean waves]]', '[[soft rain]]']
            else:
                return ['[[bell]]', '[[singing bowl]]']
        elif phase == 'completion':
            return ['[[gentle bell]]', '[[settling silence]]']
        
        return []

    def _identify_focus_areas(self, user_input: str) -> List[str]:
        """Identify what aspects of the user's experience to focus on."""
        
        focus_areas = []
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['feel', 'feeling', 'felt']):
            focus_areas.append('sensation')
        if any(word in user_lower for word in ['breath', 'breathing']):
            focus_areas.append('breath')
        if any(word in user_lower for word in ['think', 'thought', 'mind']):
            focus_areas.append('mental_activity')
        if any(word in user_lower for word in ['body', 'chest', 'heart', 'shoulders']):
            focus_areas.append('body_awareness')
        
        return focus_areas if focus_areas else ['presence']


def integrate_contextual_behavior(user_input: str, conversation_history: List[Dict], 
                                reflection_logger=None) -> Dict:
    """
    Main integration function that analyzes context and provides guidance
    for generating appropriate responses.
    """
    
    analyzer = ContextualBehaviorAnalyzer()
    generator = ContextualResponseGenerator()
    
    # Analyze the current context
    context_analysis = analyzer.analyze_conversation_context(
        conversation_history, user_input
    )
    
    # Generate response guidance
    response_guidance = generator.generate_contextual_response(
        context_analysis, user_input
    )
    
    # Log contextual insights if reflection logger is available
    if reflection_logger:
        reflection_logger.log_ai_reflection(
            'contextual_analysis',
            f"Context: {context_analysis['conversation_phase']} phase, "
            f"{context_analysis['presence_level']} presence, "
            f"{context_analysis['emotional_tone']} tone",
            user_prompt=user_input
        )
    
    return {
        'context_analysis': context_analysis,
        'response_guidance': response_guidance,
        'behavioral_adaptations': {
            'pacing': context_analysis['pacing_needs'],
            'presence_focus': response_guidance['presence_focus'],
            'ambient_support': response_guidance['ambient_cues'],
            'natural_closure': response_guidance['offer_soft_exit']
        }
    }
