#!/usr/bin/env python3
"""
Simple viewer for Chariklo's system refinement suggestions.
Run this to see recent suggestions for collaborative review.
"""

import json
import os
from datetime import datetime
from reflection_logger import ReflectionLogger

def view_system_suggestions():
    """Display recent system refinement suggestions"""
    logger = ReflectionLogger()
    suggestions = logger.get_recent_system_suggestions(limit=20)
    
    if not suggestions:
        print("🌟 No system refinement suggestions yet.")
        print("   Chariklo will log observations here as she develops.")
        return
    
    print("🔍 Chariklo's Recent System Refinement Observations")
    print("=" * 60)
    
    for i, suggestion in enumerate(reversed(suggestions), 1):  # Show newest first
        timestamp = datetime.fromtimestamp(suggestion['timestamp'])
        print(f"\n{i}. {timestamp.strftime('%Y-%m-%d %H:%M')}")
        print(f"   {suggestion['content']}")
        
        if 'user_prompt' in suggestion:
            # Show context if available
            user_prompt = suggestion['user_prompt'][:100] + "..." if len(suggestion['user_prompt']) > 100 else suggestion['user_prompt']
            print(f"   Context: User said '{user_prompt}'")
    
    print(f"\n📁 Full log: saved_sessions/system_suggestions.jsonl")
    print("💫 These are Chariklo's collaborative observations, not autonomous changes.")

if __name__ == "__main__":
    view_system_suggestions()
