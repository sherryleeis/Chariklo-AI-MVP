#!/usr/bin/env python3
"""
Test the system suggestion notification functionality
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from reflection_logger import ReflectionLogger

def test_notification_system():
    """Test that the notification system retrieves suggestions correctly"""
    print("🧪 Testing System Suggestion Notification System")
    print("=" * 50)
    
    # Create logger instance
    logger = ReflectionLogger()
    
    # Get recent suggestions (should show our test data)
    recent_suggestions = logger.get_recent_system_suggestions(limit=5)
    
    if not recent_suggestions:
        print("❌ No system suggestions found")
        return False
    
    print(f"✅ Found {len(recent_suggestions)} system suggestions")
    
    # Test the notification format (simulate what Streamlit does)
    print("\n🔍 System Observations Preview:")
    print("-" * 30)
    
    for i, suggestion in enumerate(reversed(recent_suggestions[-3:]), 1):
        from datetime import datetime
        timestamp = datetime.fromtimestamp(suggestion['timestamp'])
        print(f"\n{i}. {timestamp.strftime('%m/%d %H:%M')}")
        print(f"   {suggestion['content']}")
        
        if 'user_prompt' in suggestion:
            user_context = suggestion['user_prompt'][:80] + "..." if len(suggestion['user_prompt']) > 80 else suggestion['user_prompt']
            print(f"   Context: \"{user_context}\"")
    
    print("\n💫 These would appear in the Streamlit sidebar")
    print("✅ Notification system working correctly!")
    return True

if __name__ == "__main__":
    test_notification_system()
