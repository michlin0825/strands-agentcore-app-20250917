#!/usr/bin/env python3
"""
Test script for HelloWorld Strands Agent
Tests both single-turn and multi-turn conversations
"""

import requests
import json
import time
import uuid

# Configuration
BASE_URL = "http://localhost:8080"
SESSION_ID = f"test-session-{uuid.uuid4().hex[:8]}"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/ping")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def send_message(prompt, session_id=None):
    """Send a message to the agent"""
    payload = {"prompt": prompt}
    if session_id:
        payload["session_id"] = session_id
    
    try:
        response = requests.post(
            f"{BASE_URL}/invocations",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

def test_single_turn():
    """Test single-turn conversation"""
    print("\n🔍 Testing single-turn conversation...")
    
    response = send_message("Hello! What can you help me with?")
    if response and response.get("status") == "success":
        print("✅ Single-turn test passed")
        print(f"Response: {response.get('response', '')[:100]}...")
        return True
    else:
        print("❌ Single-turn test failed")
        return False

def test_multi_turn():
    """Test multi-turn conversation with memory"""
    print(f"\n🔍 Testing multi-turn conversation (Session: {SESSION_ID})...")
    
    # First message - introduce name
    print("📤 Sending: 'Hi, my name is Alice and I love cooking'")
    response1 = send_message("Hi, my name is Alice and I love cooking", SESSION_ID)
    
    if not response1 or response1.get("status") != "success":
        print("❌ First message failed")
        return False
    
    print(f"📥 Response 1: {response1.get('response', '')[:100]}...")
    
    # Wait a moment for memory to be stored
    time.sleep(2)
    
    # Second message - test memory recall
    print("📤 Sending: 'What is my name and what do I like?'")
    response2 = send_message("What is my name and what do I like?", SESSION_ID)
    
    if not response2 or response2.get("status") != "success":
        print("❌ Second message failed")
        return False
    
    print(f"📥 Response 2: {response2.get('response', '')[:100]}...")
    
    # Check if the agent remembered the name and hobby
    response_text = response2.get('response', '').lower()
    if 'alice' in response_text and 'cook' in response_text:
        print("✅ Multi-turn test passed - Agent remembered context!")
        return True
    else:
        print("❌ Multi-turn test failed - Agent didn't remember context")
        print(f"Full response: {response2.get('response', '')}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\n🔍 Testing error handling...")
    
    # Test empty prompt
    response = send_message("")
    if response and "error" in response:
        print("✅ Error handling test passed")
        return True
    else:
        print("❌ Error handling test failed")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting HelloWorld Strands Agent Tests")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Single Turn", test_single_turn),
        ("Multi Turn", test_multi_turn),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Your agent is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs and configuration.")

if __name__ == "__main__":
    main()
