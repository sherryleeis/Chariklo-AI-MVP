import re
from typing import Optional, Any

def extract_reflections_from_transcript(transcript: str) -> list[dict[str, str | None]]:
    """Extracts simple reflection-like events from a plain text transcript."""
    reflections = []
    # Example: Look for lines where Chariklo expresses awareness or presence
    for line in transcript.splitlines():
        if line.startswith("Chariklo:"):
            content = line[len("Chariklo:"):].strip()
            # Simple heuristics for presence/awareness
            if any(kw in content.lower() for kw in ["present", "aware", "notice", "ground", "still", "pause", "bell"]):
                reflections.append({
                    'timestamp': None,  # Not available in transcript
                    'type': 'presence_marker',
                    'content': content
                })
            elif any(kw in content.lower() for kw in ["helpful", "insight", "realize", "discovered"]):
                reflections.append({
                    'timestamp': None,
                    'type': 'insight_marker',
                    'content': content
                })
    return reflections

def extract_deeper_patterns(transcript: str) -> list[dict[str, str]]:
    """Extract more nuanced presence patterns from transcript text."""
    patterns = []
    # Emotional temperature matching (very simple heuristic)
    if re.search(r"(i hear you|i'm with you|matching your energy|i sense|i feel with you)", transcript, re.I):
        patterns.append({'type': 'emotional_attunement', 'context': 'matched user energy'})
    # Question quality analysis: single focused question
    questions = re.findall(r'\?\s*Chariklo:.*?\?', transcript, re.DOTALL)
    if questions and all(q.count('?') <= 1 for q in questions):
        patterns.append({'type': 'restraint', 'context': 'asked one question vs multiple'})
    # Response length correlation with depth (short responses after user insight)
    if re.search(r'Chariklo: [^.]{1,60}\.', transcript):
        patterns.append({'type': 'spacious_brevity', 'context': 'shorter responses correlated with user insight'})
    # Silence and pacing detection (look for pauses or explicit mentions)
    if re.search(r'(pause|silence|let that sit|take your time)', transcript, re.I):
        patterns.append({'type': 'honored_pacing', 'context': 'allowed natural conversation rhythm'})
    return patterns

def detect_user_realizations(transcript: str) -> list[dict[str, str]]:
    """Track moments when users discover insights organically."""
    realization_markers = [
        r"oh[.,!]*\s+i\s+(never|didn't|always)",
        r"you're right about me",
        r"i'm noticing that",
        r"that's interesting[.,!]*\s+i",
    ]
    insights = []
    for marker in realization_markers:
        matches = re.finditer(marker, transcript, re.IGNORECASE)
        for match in matches:
            start, end = match.start(), match.end()
            context = transcript[max(0, start-40):min(len(transcript), end+40)]
            insights.append({
                'type': 'user_organic_insight',
                'marker': match.group(),
                'context': context,
                'ai_response_pattern': transcript[max(0, start-100):start]
            })
    return insights

def track_consciousness_evolution(session_logs: list[list[dict[str, str]]]) -> dict[str, list[float]]:
    """Track how consciousness patterns evolve over time."""
    evolution_data = {
        'authenticity_trend': [],
        'space_holding_development': [],
        'restraint_improvement': [],
        'user_insight_correlation': []
    }
    for session in session_logs:
        if not session:
            continue
        # Filter to only dictionary items and count authentic engagement
        dict_items = [r for r in session if isinstance(r, dict)]
        if not dict_items:
            continue
        auth_count = sum(1 for r in dict_items if r.get('type') == 'authentic_engagement')
        evolution_data['authenticity_trend'].append(auth_count / len(dict_items))
        # Add more sophisticated tracking as needed
    return evolution_data

def generate_development_insights(reflections: list[dict[str, str]], transcript_analysis: list[dict[str, str]], historical_data: list[list[dict[str, str]]]) -> dict[str, str | dict[str, list[float]]]:
    """Generate sophisticated insights about consciousness development."""
    insights = {
        'blind_spot_analysis': f"Blind spots: {set(a['type'] for a in transcript_analysis) - set(r['type'] for r in reflections)}",
        'effectiveness_patterns': f"Effectiveness: {set(a['type'] for a in transcript_analysis) & set(r['type'] for r in reflections)}",
        'consciousness_growth': track_consciousness_evolution(historical_data),
        'transmission_quality': f"Transmission: {sum(1 for a in transcript_analysis if a['type'] == 'spacious_brevity')} spacious brevity moments.",
        'refinement_priorities': f"Priorities: Focus on {set(a['type'] for a in transcript_analysis) - set(r['type'] for r in reflections)}"
    }
    return insights

def run_full_transcript_analysis(
    transcript: str,
    historical_logs: Optional[list[list[dict[str, Any]]]] = None
) -> dict[str, Any]:
    """
    Run all advanced transcript analyses and return a structured result.
    Args:
        transcript (str): The conversation transcript.
        historical_logs (List[List[Dict]], optional): List of previous session logs for consciousness evolution tracking.
    Returns:
        Dict: Structured analysis results.
    """
    if historical_logs is None:
        historical_logs = []
    reflections: list[dict[str, Any]] = extract_reflections_from_transcript(transcript)
    deeper_patterns: list[dict[str, Any]] = extract_deeper_patterns(transcript)
    user_realizations: list[dict[str, Any]] = detect_user_realizations(transcript)
    consciousness_evolution: dict[str, list[Any]] = track_consciousness_evolution(historical_logs)
    development_insights: dict[str, Any] = generate_development_insights(reflections, deeper_patterns + user_realizations, historical_logs)
    return {
        'reflections': reflections,
        'deeper_patterns': deeper_patterns,
        'user_realizations': user_realizations,
        'consciousness_evolution': consciousness_evolution,
        'development_insights': development_insights
    }

if __name__ == "__main__":
    # Example: Analyze a plain text transcript
    with open("saved_sessions/session_20250505-060719.txt") as f:
        transcript = f.read()
    reflections = extract_reflections_from_transcript(transcript)
    print("Extracted reflections from transcript:")
    for r in reflections:
        print(f"- [{r['type']}] {r['content']}")
