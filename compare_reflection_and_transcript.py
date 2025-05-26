import json
import glob
import os
from analyze_transcript import extract_reflections_from_transcript
from analyze_reflections import analyze_reflection_patterns, suggest_prompt_refinements

def get_latest_file(pattern):
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

# --- CONFIG ---
# Automatically use the latest .json reflection log and .txt transcript
REFLECTION_LOG_PATH = get_latest_file("saved_sessions/*.json")
TRANSCRIPT_PATH = get_latest_file("saved_sessions/*.txt")

def compare_reflections_and_transcript(reflections, transcript_markers):
    """Compare conscious reflections with transcript markers and output insights."""
    insights = []
    # 1. Types present in transcript but not in reflections (blind spots)
    transcript_types = set(m['type'] for m in transcript_markers)
    reflection_types = set(r['type'] for r in reflections)
    for ttype in transcript_types - reflection_types:
        insights.append(f"Pattern '{ttype}' appears in transcript but is not consciously logged. Possible blind spot.")
    # 2. Types present in both (confirmation)
    for ttype in transcript_types & reflection_types:
        insights.append(f"Pattern '{ttype}' is both observed and consciously logged. Self-awareness confirmed.")
    # 3. Types in reflections but not transcript (possible over-attribution)
    for rtype in reflection_types - transcript_types:
        insights.append(f"Pattern '{rtype}' is consciously logged but not observed in transcript. Possible over-attribution or missed detection.")
    return insights

# Patch: If the reflection log is a transcript, extract markers for both
if __name__ == "__main__":
    if not REFLECTION_LOG_PATH or not TRANSCRIPT_PATH:
        print("No reflection log or transcript found in saved_sessions/.")
    else:
        # Try to load reflection log as JSON, else treat as transcript
        try:
            with open(REFLECTION_LOG_PATH) as f:
                reflections = json.load(f)
        except Exception:
            with open(REFLECTION_LOG_PATH) as f:
                transcript = f.read()
            reflections = extract_reflections_from_transcript(transcript)
        # Load transcript and extract markers
        try:
            with open(TRANSCRIPT_PATH) as f:
                transcript = f.read()
            transcript_markers = extract_reflections_from_transcript(transcript)
        except Exception as e:
            print(f"Could not load transcript: {e}")
            transcript_markers = []
        # Analyze patterns in reflections
        patterns = analyze_reflection_patterns(reflections)
        # Compare and output insights
        print("\n--- Comparison Insights ---")
        insights = compare_reflections_and_transcript(reflections, transcript_markers)
        for insight in insights:
            print("-", insight)
        # Suggest prompt refinements
        print("\n--- Prompt Suggestions ---")
        suggestions = suggest_prompt_refinements(patterns)
        for suggestion in suggestions:
            print("-", suggestion)
