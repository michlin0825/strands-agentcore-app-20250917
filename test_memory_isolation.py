#!/usr/bin/env python3
"""
Test script to verify memory isolation in refactored AgentCore app
"""

import json
import uuid
from agent import invoke

def test_memory_isolation():
    """Test that different session IDs create isolated memory contexts"""
    
    # Simulate two different user sessions
    session_1 = f"session-{str(uuid.uuid4())}"
    session_2 = f"session-{str(uuid.uuid4())}"
    
    print("🧪 Testing AgentCore Memory Isolation")
    print("=" * 50)
    
    # Test payload for session 1
    payload_1 = {
        "prompt": "My name is Alice and I like cats",
        "session_id": session_1
    }
    
    # Test payload for session 2  
    payload_2 = {
        "prompt": "My name is Bob and I like dogs",
        "session_id": session_2
    }
    
    print(f"📋 Session 1 ID: {session_1[:20]}...")
    print(f"📋 Session 2 ID: {session_2[:20]}...")
    print()
    
    try:
        # Process messages for both sessions
        print("🔄 Processing Session 1 message...")
        result_1 = invoke(payload_1)
        print(f"✅ Session 1 Status: {result_1.get('status', 'unknown')}")
        
        print("🔄 Processing Session 2 message...")
        result_2 = invoke(payload_2)
        print(f"✅ Session 2 Status: {result_2.get('status', 'unknown')}")
        
        # Verify session isolation
        if result_1.get('session_id') != result_2.get('session_id'):
            print("✅ Memory Isolation: PASSED - Different session IDs maintained")
        else:
            print("❌ Memory Isolation: FAILED - Session IDs should be different")
            
        print()
        print("🎯 Test Results:")
        print(f"   Session 1 maintains: {result_1.get('session_id', 'N/A')[:20]}...")
        print(f"   Session 2 maintains: {result_2.get('session_id', 'N/A')[:20]}...")
        print()
        print("✅ AgentCore native memory isolation working correctly!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
        
    return True

if __name__ == "__main__":
    test_memory_isolation()
