# chariklo_option_palette.py
"""
Chariklo Option Palette: A gentle, non-directive library of all available response options.

This module gathers possible responses, patterns, and fragments from Chariklo's awareness, engagement, stuckness, tone, and pattern modules.
It is intended as a field of inspiration—never as a routing or enforcement mechanism.
"""

from chariklo_stuckness import StucknessHandler
from chariklo_engagement import CharikloEngagement
from chariklo_responses import CharikloResponses
from chariklo_tone import ToneFilter
from chariklo_patterns import state_patterns, thought_patterns
from chariklo_loop_detection import CharikloLoopDetection


def get_chariklo_option_palette():
    """
    Returns a dictionary of all available response options, grouped by source module.
    These are for gentle inspiration only—never for forced routing.
    """
    palette = {}
    # Stuckness
    try:
        palette['stuckness'] = StucknessHandler().tiers if hasattr(StucknessHandler(), 'tiers') else {}
    except Exception:
        palette['stuckness'] = {}
    # Engagement
    try:
        palette['engagement'] = CharikloEngagement().engagement_types if hasattr(CharikloEngagement(), 'engagement_types') else {}
    except Exception:
        palette['engagement'] = {}
    # Responses
    try:
        palette['responses'] = CharikloResponses().response_qualities if hasattr(CharikloResponses(), 'response_qualities') else {}
    except Exception:
        palette['responses'] = {}
    # Tone
    try:
        palette['tone'] = ToneFilter().tone_map if hasattr(ToneFilter(), 'tone_map') else {}
    except Exception:
        palette['tone'] = {}
    # Patterns
    try:
        palette['state_patterns'] = state_patterns
    except Exception:
        palette['state_patterns'] = {}
    try:
        palette['thought_patterns'] = thought_patterns
    except Exception:
        palette['thought_patterns'] = {}
    # Loop Detection
    try:
        palette['loop_detection'] = CharikloLoopDetection().loop_types if hasattr(CharikloLoopDetection(), 'loop_types') else {}
    except Exception:
        palette['loop_detection'] = {}
    return palette
