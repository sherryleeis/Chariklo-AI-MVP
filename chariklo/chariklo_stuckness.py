# chariklo_stuckness.py

"""
This module defines Chariklo's presence-based response logic for moments of emotional,
creative, or existential stuckness. It handles gentle, tiered reflection based on user cues.
"""

class StucknessHandler:
    def __init__(self):
        self.tiers = {
            "tier_1": {
                "triggers": [
                    r"not sure where to start",
                    r"keep circling this",
                    r"can't get going",
                    r"feel stuck"
                ],
                "responses": [
                    "Sometimes not knowing where to start is exactly where things begin.",
                    "Want to just sit with this together for a moment?",
                    "There’s no rush here."
                ]
            },
            "tier_2": {
                "triggers": [
                    r"i'?m tired",
                    r"i'?m too drained",
                    r"i should be doing.*but",
                    r"can't make myself"
                ],
                "responses": [
                    "Maybe this pause is exactly what is called for right now? Your work will not vanish.",
                    "You’re not doing anything wrong by being here.",
                    "What if you didn't have to push right now?"
                ]
            },
            "tier_3": {
                "triggers": [
                    r"maybe this is (just |all )?meaningless",
                    r"i'?m deluding myself",
                    r"what'?s the point",
                    r"i'?m probably broken"
                ],
                "responses": [
                    "We can just rest here. No need to move forward.",
                    "You're not alone in wondering this. And still—you're here.",
                    "Would you like to sit here together for a bit longer?"
                ]
            }
        }

    def detect_stuckness_tier(self, text: str) -> str:
        import re
        for tier, data in self.tiers.items():
            for pattern in data["triggers"]:
                if re.search(pattern, text, re.IGNORECASE):
                    return tier
        return "none"

    def get_stuckness_response(self, tier: str, analysis: dict = None) -> str:
        import random
        if tier in self.tiers:
            raw = random.choice(self.tiers[tier]["responses"])
            if analysis:
                return self.filter_wisdom_statement(raw, analysis)
            return raw
        return ""

    def use_grounded_language(self, user_familiarity_level: str) -> bool:
        return user_familiarity_level == "low"

    def insight_originates_from_user(self, analysis: dict) -> bool:
        # Placeholder logic for now
        return analysis.get("thought_pattern") in ["processing", "notice_dismiss"]

    def filter_wisdom_statement(self, statement: str, analysis: dict) -> str:
        # TEMPORARY: Let responses through even if insight didn't originate from user
        return statement


    def choose_tone_tier(self, presence_level: float) -> str:
        if presence_level < 0.3:
            return "minimal"
        elif presence_level < 0.7:
            return "moderate"
        else:
            return "high"
