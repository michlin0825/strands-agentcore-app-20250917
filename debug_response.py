#!/usr/bin/env python3
import boto3
import json

def test_agent_response():
    session = boto3.Session(profile_name="CloudChef01")
    client = session.client('bedrock-agentcore', region_name='us-east-1')
    
    payload = json.dumps({"prompt": "What's the weather in Taipei?", "session_id": "test-session-12345678901234567890123456789012"})
    
    response = client.invoke_agent_runtime(
        agentRuntimeArn="arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgentV2-R3GAODHoRb",
        runtimeSessionId="test-session-12345678901234567890123456789012",
        payload=payload
    )
    
    response_body = response['response'].read()
    response_data = json.loads(response_body)
    
    print("=== FULL RESPONSE STRUCTURE ===")
    print(json.dumps(response_data, indent=2))
    
    print("\n=== KEYS AT ROOT LEVEL ===")
    print(list(response_data.keys()))
    
    if 'response' in response_data:
        print("\n=== KEYS IN response_data['response'] ===")
        print(list(response_data['response'].keys()))
        
        if 'content' in response_data['response']:
            print("\n=== CONTENT STRUCTURE ===")
            content = response_data['response']['content']
            print(f"Content type: {type(content)}")
            print(f"Content length: {len(content) if isinstance(content, list) else 'N/A'}")
            
            if isinstance(content, list) and len(content) > 0:
                print(f"First item type: {type(content[0])}")
                print(f"First item keys: {list(content[0].keys()) if isinstance(content[0], dict) else 'N/A'}")
                
                if isinstance(content[0], dict) and 'text' in content[0]:
                    print("\n=== EXTRACTED TEXT ===")
                    print(repr(content[0]['text']))

if __name__ == "__main__":
    test_agent_response()
