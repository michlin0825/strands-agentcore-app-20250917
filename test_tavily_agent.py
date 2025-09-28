#!/usr/bin/env python3
"""
Test script for AgentCore agent with Tavily search integration
"""

import boto3
import json
import time
from datetime import datetime

# Configuration
AWS_PROFILE = "CloudChef01"
AWS_REGION = "us-east-1"
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgentV2-R3GAODHoRb"

def test_agent_with_search():
    """Test the agent with various search scenarios"""
    
    print("🔍 Testing AgentCore Agent with Tavily Search Integration")
    print("=" * 60)
    
    # Initialize AgentCore client
    session = boto3.Session(profile_name=AWS_PROFILE)
    client = session.client('bedrock-agentcore', region_name=AWS_REGION)
    
    # Test scenarios
    test_cases = [
        {
            "name": "Basic Conversation (No Search)",
            "prompt": "Hello! My name is Sarah and I'm a software engineer.",
            "expect_search": False
        },
        {
            "name": "Current Events Search",
            "prompt": "What are the latest developments in AI technology this week?",
            "expect_search": True
        },
        {
            "name": "Factual Information Search", 
            "prompt": "What is the current stock price of NVIDIA?",
            "expect_search": True
        },
        {
            "name": "Memory + Search Combination",
            "prompt": "Based on what I told you about being a software engineer, can you find recent news about software engineering job market trends?",
            "expect_search": True
        },
        {
            "name": "Follow-up Question",
            "prompt": "What do you remember about me?",
            "expect_search": False
        }
    ]
    
    session_id = f"test-tavily-search-integration-{int(time.time())}-session"
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📍 Test {i}: {test_case['name']}")
        print("-" * 40)
        print(f"🗣️  Prompt: {test_case['prompt']}")
        
        try:
            # Call AgentCore
            response = client.invoke_agent_runtime(
                agentRuntimeArn=AGENT_RUNTIME_ARN,
                runtimeSessionId=session_id,
                payload=json.dumps({
                    'prompt': test_case['prompt'],
                    'session_id': session_id
                })
            )
            
            result = json.loads(response['response'].read())
            
            if result['status'] == 'success':
                response_text = result['response']['content'][0]['text']
                print(f"✅ Status: Success")
                print(f"🤖 Response: {str(response_text)[:200]}...")
                
                # Check if search was used
                search_indicators = [
                    "search results", "according to", "based on recent", 
                    "current", "latest", "**Direct Answer:**", "**Search Results:**"
                ]
                
                used_search = any(indicator.lower() in response_text.lower() 
                                for indicator in search_indicators)
                
                if test_case['expect_search']:
                    if used_search:
                        print("🔍 Search: ✅ Used (as expected)")
                    else:
                        print("🔍 Search: ❌ Not used (expected to use)")
                else:
                    if used_search:
                        print("🔍 Search: ⚠️  Used (not expected)")
                    else:
                        print("🔍 Search: ✅ Not used (as expected)")
                        
            else:
                print(f"❌ Status: Failed - {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Wait between tests
        if i < len(test_cases):
            print("⏳ Waiting 2 seconds...")
            time.sleep(2)
    
    print(f"\n🎉 Testing Complete!")
    print(f"Session ID: {session_id}")
    print(f"Agent ARN: {AGENT_RUNTIME_ARN}")

def test_direct_search():
    """Test direct search functionality"""
    print("\n🔍 Testing Direct Search Functionality")
    print("=" * 40)
    
    session = boto3.Session(profile_name=AWS_PROFILE)
    client = session.client('bedrock-agentcore', region_name=AWS_REGION)
    
    search_prompt = "Please search for information about the latest AWS re:Invent 2024 announcements"
    
    try:
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId=f"direct-search-test-session-{int(time.time())}-long-enough",
            payload=json.dumps({
                'prompt': search_prompt,
                'session_id': 'direct-search-test'
            })
        )
        
        result = json.loads(response['response'].read())
        
        if result['status'] == 'success':
            response_text = result['response']['content'][0]['text']
            print(f"✅ Direct Search Test Successful")
            print(f"📝 Full Response:\n{response_text}")
        else:
            print(f"❌ Direct Search Failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Direct Search Error: {e}")

if __name__ == "__main__":
    # Run basic agent tests
    test_agent_with_search()
    
    # Run direct search test
    test_direct_search()
    
    print(f"\n📋 Test Summary:")
    print(f"   - Agent Runtime: {AGENT_RUNTIME_ARN}")
    print(f"   - AWS Profile: {AWS_PROFILE}")
    print(f"   - Region: {AWS_REGION}")
    print(f"   - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
