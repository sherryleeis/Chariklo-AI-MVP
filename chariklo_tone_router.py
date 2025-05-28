# chariklo_tone_router.py
"""
Tone Router for Chariklo: routes user input to the correct tone tag for response selection.
Supports loop detection, stuckness, thought patterns, engagement, and fallback logic.
"""
from chariklo_loop_detection import CharikloLoopDetection
from chariklo_stuckness import StucknessHandler
from chariklo_patterns import detect_thought_pattern
from chariklo_engagement import detect_engagement_pattern

# Main routing function
def detect_looping(user_input):
    # Use the CharikloLoopDetection class to check for loops
    detector = CharikloLoopDetection()
    return detector.detect_loop(user_input) != "no_loop"

def detect_stuckness_tier(user_input):
    # Use the StucknessHandler class to check for stuckness tier
    handler = StucknessHandler()
    tier = handler.detect_stuckness_tier(user_input)
    if tier == "tier_3":
        return "high"
    elif tier == "tier_2":
        return "medium"
    elif tier == "tier_1":
        return "low"
    else:
        return "none"

def route_to_tone_tag(user_input, analysis=None):
    """
    Returns a tone tag string for the given user input and analysis.
    """
    # 1. Loop detection
    if detect_looping(user_input):
        return "looping-gentle"

    # 2. Stuckness detection
    stuckness = detect_stuckness_tier(user_input)
    if stuckness == "high":
        return "stuckness-high"
    elif stuckness == "medium":
        return "stuckness-medium"
    elif stuckness == "low":
        return "stuckness-low"

    # 3. Thought pattern detection
    thought_pattern = detect_thought_pattern(user_input)
    if thought_pattern:
        return f"thought-pattern-{thought_pattern}"

    # 4. Engagement & resistance
    engagement = detect_engagement_pattern(user_input)
    if engagement:
        return f"engagement-{engagement}"

    # 5. Fallback
    return "gentle-fallback"
