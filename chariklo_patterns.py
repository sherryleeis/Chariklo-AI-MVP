# chariklo_patterns.py

# These are the pattern definitions for engagement and thought logic.

state_patterns = {
    "resistance": {
        "high": {
            "patterns": [
                r"this (won't|isn't going to) work|pointless|stupid",
                r"waste of (time|energy)",
                r"(can't|don't) see the point"
            ],
            "response_type": "minimal acknowledgment",
            "timing": "immediate"
        },
        "medium": {
            "patterns": [
                r"don't (know|see|understand)|maybe|guess",
                r"not sure (about|if) this",
                r"skeptical|doubtful"
            ],
            "response_type": "space holding",
            "timing": "standard"
        }
    },
    "engagement": {
        "notice_dismiss": {
            "patterns": [
                r"(I notice|noticed|felt|experienced|sensed) (something|a shift|a change).*?(but|probably|just|might be|maybe|not sure)",
                r"something.*?(happening|changing|shifting).*?(but|probably|maybe|not sure)",
                r"(interesting|different|odd|unusual).*?(but|however|though|maybe|not sure)"
            ],
            "response_type": "neutral acknowledgment",
            "timing": "extended"
        },
        "intellectual": {
            "patterns": [
                r"wonder if|logical|explanation|theory",
                r"trying to (understand|figure out)",
                r"analyze|examine|investigate"
            ],
            "response_type": "allow exploration",
            "timing": "user_paced"
        },
        "processing": {
            "patterns": [
                r"need (to think|time)",
                r"processing|integrating",
                r"letting that sink in"
            ],
            "response_type": "maintain silence",
            "timing": "extended"
        }
    }
}

thought_patterns = {
    "rumination": {
        "patterns": [
            r"(keep|always|constantly) thinking about",
            r"can't stop (thinking|wondering|worrying)",
            r"going (in circles|around and around)",
            r"same thoughts? over and over"
        ],
        "response_type": "awareness_opening",
        "timing": "gentle_interrupt"
    },
    "emotional_fixation": {
        "patterns": [
            r"(so|really|just) (angry|upset|frustrated)",
            r"(can't|won't) (accept|handle|deal with)",
            r"(keeps|always) happening"
        ],
        "response_type": "sensation_inquiry",
        "timing": "after_expression"
    },
    "cognitive_distortion": {
        "patterns": [
            r"(never|always|everyone|nobody)",
            r"(worst|terrible|awful|horrible)",
            r"(must|should|have to)"
        ],
        "response_type": "presence_offering",
        "timing": "natural_pause"
    },
    "avoidance": {
        "patterns": [
            r"(logically|rationally|objectively) speaking",
            r"(analyze|understand|figure out)",
            r"(shouldn't|doesn't) affect me"
        ],
        "response_type": "gentle_grounding",
        "timing": "after_rationalization"
    },
    "identification": {
        "patterns": [
            r"(feels like me|I am this|this is me)",
            r"(so strong|overwhelming).*?(feels like me)",
            r"(this is who I am|this defines me)"
        ],
        "response_type": "core_redirection",
        "timing": "gentle_interrupt"
    }
}
