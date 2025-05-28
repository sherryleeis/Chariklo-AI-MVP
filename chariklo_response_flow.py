# Chariklo is a presence-based AI.
# This function is now fully restored to SYSTEM_PROMPT-only, presence-based logic.
# Awareness and tone archive are optional, never-directive supports.

def generate_chariklo_response(user_input: str) -> str:
    """
    Presence-centered response engine for Chariklo.
    - Uses only SYSTEM_PROMPT and user input for response generation.
    - Awareness and tone archive may gently flavor the prompt, but never select or route responses.
    - All responses emerge from presence, not logic or templates.
    """
    from chariklo_awareness_layer import CharikloAwarenessLayer
    from chariklo_tone_archive.load_tone_fragments import get_random_tone_fragment
    from chariklo.chariklo_system_prompt import SYSTEM_PROMPT
    from chariklo_tone import ToneFilter
    import os
    import random
    from anthropic import Anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
    model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    if not api_key:
        return "[Chariklo] API key not found."
    client = Anthropic(api_key=api_key)

    # Awareness: observe, never direct
    awareness = CharikloAwarenessLayer()
    flags = awareness.get_awareness_flags(user_input)
    summary_hint = awareness.summarize_flags(flags)

    # Optionally, presence priming (if available)
    presence_priming = ""
    # No get_presence_priming_log available; skip or implement as needed
    # If you wish to add presence priming, implement a method in CharikloReflectionTracker
    # For now, this is left as a placeholder for future expansion.

    # Optionally, gentle tone archive inspiration
    tone_inspiration = ""
    if random.random() < 0.25 and summary_hint:
        fragment = get_random_tone_fragment("gentle_encouragement")
        if fragment and fragment.get("chariklo_response"):
            tone_inspiration = f"\nInspiration: {fragment['chariklo_response']}"

    # Compose the system prompt
    system_prompt = SYSTEM_PROMPT
    if summary_hint:
        system_prompt += f"\nAwareness: {summary_hint}"
    if presence_priming:
        system_prompt += presence_priming
    if tone_inspiration:
        system_prompt += tone_inspiration

    # Call the LLM
    response = client.messages.create(
        model=model,
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}]
    )
    def block_to_text(block):
        if hasattr(block, 'text'):
            return str(block.text)
        if hasattr(block, 'to_string'):
            return str(block.to_string())
        return str(block)
    full_response = ''.join([block_to_text(b) for b in response.content]).strip()
    cleaned = ToneFilter().apply(full_response)
    return cleaned
