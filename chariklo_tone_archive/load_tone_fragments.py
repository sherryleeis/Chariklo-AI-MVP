import os
import json
import random
from pathlib import Path
from collections import defaultdict, deque

# Short-term memory for recently used fragments (per response_type)
_recent_fragments = defaultdict(lambda: deque(maxlen=5))

def reset_recent_tone_fragments():
    """Reset the recent fragment memory (call at session end)."""
    _recent_fragments.clear()

def load_tone_fragments_by_response_type(response_type, archive_dir="chariklo_tone_archive"):
    """
    Loads all tone fragments from the archive directory that match the given response_type.
    Returns a list of matching fragments (dicts).
    Handles both single-object and list-of-object JSON files.
    """
    archive_path = Path(archive_dir)
    fragments = []
    for file in archive_path.glob("*.json"):
        try:
            with open(file, "r") as f:
                data = json.load(f)
                # Support both single-object and list-of-object files
                if isinstance(data, dict):
                    data = [data]
                for fragment in data:
                    if fragment.get("response_type") == response_type:
                        fragments.append(fragment)
        except Exception as e:
            print(f"Error loading {file}: {e}")
    print(f"[DEBUG] Loaded {len(fragments)} fragments for response_type '{response_type}'")
    return fragments

def get_random_tone_fragment(response_type, archive_dir="chariklo_tone_archive", presence_level=None):
    """
    Returns a random fragment dict for the given response_type, excluding recently used ones.
    """
    matches = load_tone_fragments_by_response_type(response_type, archive_dir)
    recent_ids = set(_recent_fragments[response_type])
    available = [frag for frag in matches if frag.get("id") not in recent_ids]
    print(f"[DEBUG] Available fragments for '{response_type}': {[f.get('id') for f in available]}")
    print(f"[DEBUG] Recently used for '{response_type}': {list(_recent_fragments[response_type])}")
    if not available:
        # If all have been used, reset memory for this type and use all
        _recent_fragments[response_type].clear()
        available = matches
        print(f"[DEBUG] All fragments used for '{response_type}', resetting memory.")
    if available:
        chosen = random.choice(available)
        frag_id = chosen.get("id")
        if frag_id:
            _recent_fragments[response_type].append(frag_id)
        print(f"[DEBUG] Chosen fragment for '{response_type}': {frag_id}")
        return chosen
    print(f"[DEBUG] No available fragments for '{response_type}'")
    return None

# Example usage:
if __name__ == "__main__":
    frag = get_random_tone_fragment("perception_broadening")
    if frag:
        print(frag["chariklo_response"])
    else:
        print("No matching fragment found.")
