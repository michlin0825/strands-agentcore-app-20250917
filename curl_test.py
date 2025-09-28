#!/usr/bin/env python3
import boto3
import json
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

# Configuration
AWS_PROFILE = "CloudChef01"
REGION = "us-east-1"
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgent-EqFCwr3WrQ"

def test_with_signed_request():
    """Test using signed HTTP request"""
    print("🌐 Testing AgentCore with signed HTTP request...")
    
    # Get credentials
    session = boto3.Session(profile_name=AWS_PROFILE)
    credentials = session.get_credentials()
    
    # Prepare request
    url = f"https://bedrock-agentcore.{REGION}.amazonaws.com/runtime/HelloWorldStrandsAgent-EqFCwr3WrQ/invocations"
    payload = json.dumps({
        "prompt": "Hello from curl test!",
        "session_id": "curl-test-12345678901234567890123456789012"
    })
    
    # Create AWS request
    request = AWSRequest(
        method='POST',
        url=url,
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'X-Amz-Target': 'InvokeAgentRuntime'
        }
    )
    
    # Sign the request
    SigV4Auth(credentials, 'bedrock-agentcore', REGION).add_auth(request)
    
    print(f"📤 URL: {url}")
    print(f"📤 Payload: {payload}")
    print(f"📤 Headers: {dict(request.headers)}")
    
    # Make the request
    try:
        response = requests.post(
            url,
            data=payload,
            headers=dict(request.headers)
        )
        
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
        else:
            print("❌ Failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_with_signed_request()
