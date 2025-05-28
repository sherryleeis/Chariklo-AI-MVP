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
import os
import json


def load_all_tone_fragments(archive_dir="chariklo_tone_archive"):
    """
    Loads all tone fragments from the archive directory and returns them as a list of dicts.
    """
    archive_path = archive_dir if os.path.isabs(archive_dir) else os.path.join(os.path.dirname(__file__), archive_dir)
    fragments = []
    if not os.path.exists(archive_path):
        return fragments
    for file in os.listdir(archive_path):
        if file.endswith(".json"):
            try:
                with open(os.path.join(archive_path, file), "r") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        fragments.append(data)
                    elif isinstance(data, list):
                        fragments.extend(data)
            except Exception:
                continue
    return fragments


def get_chariklo_option_palette():
    """
    Returns a dictionary of all available response options, grouped by source module.
    These are for gentle inspiration only—never for forced routing.
    """
    palette = {}
    # Stuckness
    try:
        palette['stuckness'] = getattr(StucknessHandler(), 'tiers', {})
    except Exception:
        palette['stuckness'] = {}
    # Engagement
    try:
        palette['engagement'] = getattr(CharikloEngagement(), 'state_patterns', {})
    except Exception:
        palette['engagement'] = {}
    # Responses
    try:
        palette['responses'] = getattr(CharikloResponses(), 'response_qualities', {})
    except Exception:
        palette['responses'] = {}
    # Tone
    try:
        palette['tone'] = getattr(ToneFilter(), 'softened_terms', {})
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
        palette['loop_detection'] = getattr(CharikloLoopDetection(), 'validation_patterns', {})
    except Exception:
        palette['loop_detection'] = {}
    # Tone Archive (all fragments, non-directive, browsable)
    try:
        palette['tone_archive'] = load_all_tone_fragments()
    except Exception:
        palette['tone_archive'] = []
    return palette
