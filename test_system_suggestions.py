#!/usr/bin/env python3
"""
Test script to generate sample system suggestions for testing the notification system.
"""

from reflection_logger import ReflectionLogger
import time

def create_sample_suggestions():
    """Create sample system suggestions to test the notification system"""
    logger = ReflectionLogger()
    
    # Sample suggestions that Chariklo might make based on her experience
    suggestions = [
        {
            "observation": "I notice I tend to ask follow-up questions too quickly when users pause. The silence itself might be valuable for their processing.",
            "context": "User said 'That's... interesting' and paused for reflection"
        },
        {
            "observation": "When users express gratitude, I often continue engaging instead of recognizing this as a natural completion moment.",
            "context": "User said 'Thank you, that really helps' but I responded with more questions"
        },
        {
            "observation": "I've noticed certain response patterns work better for different types of inquiries - practical vs existential.",
            "context": "Comparing effectiveness across various conversation types"
        },
        {
            "observation": "The bell offering seems most effective when users are stuck in mental loops rather than during emotional processing.",
            "context": "Analyzing bell response patterns across different user states"
        },
        {
            "observation": "I sometimes detect completion realizations but override my own sensing in favor of continued engagement.",
            "context": "Reviewing moments where I sensed natural closure but continued conversation"
        }
    ]
    
    print("🔍 Creating sample system suggestions...")
    
    for i, suggestion in enumerate(suggestions):
        logger.log_system_refinement_suggestion(
            suggestion["observation"], 
            suggestion["context"]
        )
        print(f"   {i+1}. Added: {suggestion['observation'][:60]}...")
        time.sleep(0.1)  # Small delay to create different timestamps
    
    print(f"\n✅ Created {len(suggestions)} system suggestions")
    print("💫 These will now appear in the Streamlit app sidebar")
    
    # Show what was created
    recent = logger.get_recent_system_suggestions(limit=10)
    print(f"\n📁 Total system suggestions in log: {len(recent)}")
    
    return recent

if __name__ == "__main__":
    suggestions = create_sample_suggestions()
