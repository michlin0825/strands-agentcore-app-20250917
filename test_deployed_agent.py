#!/usr/bin/env python3
"""
Test script for deployed Strands AgentCore App on AgentCore Runtime
"""

import boto3
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment
AWS_PROFILE = os.getenv('AWS_PROFILE', 'CloudChef01')
REGION = os.getenv('AWS_REGION', 'us-east-1')
AGENT_RUNTIME_ARN = os.getenv('AGENT_RUNTIME_ARN')

if not AGENT_RUNTIME_ARN:
    print("❌ Error: AGENT_RUNTIME_ARN environment variable not set")
    print("Please check your .env file")
    exit(1)

def test_agent():
    """Test the deployed agent with multiple calls"""
    print("🧪 Testing Strands AgentCore App on AgentCore Runtime")
    print("=" * 60)
    
    # Initialize client
    session = boto3.Session(profile_name=AWS_PROFILE)
    client = session.client('bedrock-agentcore', region_name=REGION)
    
    # Test cases
    test_cases = [
        {
            "name": "Basic Greeting",
            "prompt": "Hello! My name is Alice and I love cooking.",
            "session_id": "test-session-alice-12345678901234567890123456789012"
        },
        {
            "name": "Memory Test",
            "prompt": "What is my name and what do I like?",
            "session_id": "test-session-alice-12345678901234567890123456789012"
        },
        {
            "name": "Technical Question",
            "prompt": "Explain what AWS Lambda is in simple terms.",
            "session_id": "test-session-tech-12345678901234567890123456789012"
        },
        {
            "name": "Creative Task",
            "prompt": "Write a short poem about artificial intelligence.",
            "session_id": "test-session-creative-12345678901234567890123456789012"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print(f"📤 Prompt: {test_case['prompt']}")
        print(f"🆔 Session: {test_case['session_id'][:20]}...")
        
        try:
            # Prepare payload
            payload = json.dumps({
                "prompt": test_case["prompt"],
                "session_id": test_case["session_id"]
            })
            
            # Invoke agent
            start_time = time.time()
            response = client.invoke_agent_runtime(
                agentRuntimeArn=AGENT_RUNTIME_ARN,
                runtimeSessionId=test_case["session_id"],
                payload=payload
            )
            end_time = time.time()
            
            # Parse response
            response_body = response['response'].read()
            response_data = json.loads(response_body)
            
            # Display results
            if response_data.get('status') == 'success':
                print(f"✅ Success ({end_time - start_time:.2f}s)")
                response_content = response_data.get('response', {})
                if isinstance(response_content, dict) and 'content' in response_content:
                    content = response_content['content']
                    if isinstance(content, list) and len(content) > 0:
                        text = content[0].get('text', 'No text content')
                    else:
                        text = str(content)
                else:
                    text = str(response_content)
                print(f"📥 Response: {str(text)[:200]}...")
                results.append({
                    "test": test_case['name'],
                    "status": "success",
                    "response_time": end_time - start_time,
                    "response": text
                })
            else:
                print(f"❌ Failed: {response_data}")
                results.append({
                    "test": test_case['name'],
                    "status": "failed",
                    "error": response_data
                })
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "test": test_case['name'],
                "status": "error",
                "error": str(e)
            })
        
        # Wait between tests
        if i < len(test_cases):
            time.sleep(2)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    successful_tests = [r for r in results if r['status'] == 'success']
    failed_tests = [r for r in results if r['status'] != 'success']
    
    print(f"✅ Successful: {len(successful_tests)}/{len(test_cases)}")
    print(f"❌ Failed: {len(failed_tests)}/{len(test_cases)}")
    
    if successful_tests:
        avg_response_time = sum(r['response_time'] for r in successful_tests) / len(successful_tests)
        print(f"⏱️  Average Response Time: {avg_response_time:.2f}s")
    
    # Show detailed results
    print(f"\n📋 Detailed Results:")
    for result in results:
        status_icon = "✅" if result['status'] == 'success' else "❌"
        print(f"  {status_icon} {result['test']}: {result['status']}")
        if result['status'] == 'success':
            response_text = str(result.get('response', ''))
            print(f"     Response: {response_text[:100]}...")
        elif 'error' in result:
            print(f"     Error: {result['error']}")
    
    print(f"\n🎯 Agent Runtime ARN: {AGENT_RUNTIME_ARN}")
    print(f"🌍 Region: {REGION}")
    print(f"👤 Profile: {AWS_PROFILE}")
    
    return len(successful_tests) == len(test_cases)

if __name__ == "__main__":
    success = test_agent()
    if success:
        print("\n🎉 All tests passed! Your agent is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above for details.")
