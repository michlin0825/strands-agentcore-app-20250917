#!/usr/bin/env python3
"""
Simple test for deployed agent with Claude 3 Haiku
"""

import boto3
import json

# Configuration
AWS_PROFILE = "CloudChef01"
REGION = "us-east-1"
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgent-EqFCwr3WrQ"

def test_simple():
    """Simple test with Claude 3 Haiku model override"""
    print("🧪 Simple Test - HelloWorld Strands Agent")
    print("=" * 50)
    
    # Initialize client
    session = boto3.Session(profile_name=AWS_PROFILE)
    client = session.client('bedrock-agentcore', region_name=REGION)
    
    try:
        # Prepare payload with model override
        payload = json.dumps({
            "prompt": "Hello! Just say 'Hi there!' to test the connection.",
            "session_id": "simple-test-12345678901234567890123456789012"
        })
        
        print(f"📤 Testing with payload: {payload}")
        
        # Invoke agent
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId="simple-test-12345678901234567890123456789012",
            payload=payload
        )
        
        # Parse response
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        
        print(f"📥 Raw response: {response_data}")
        
        if response_data.get('status') == 'success':
            print("✅ SUCCESS! Agent is working!")
            print(f"Response: {response_data.get('response', '')}")
        else:
            print(f"❌ Failed: {response_data}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple()
