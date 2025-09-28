#!/usr/bin/env python3
"""
Force update AgentCore Runtime with new container image
"""

import boto3
import json
import time

# Configuration
AWS_PROFILE = "CloudChef01"
AWS_REGION = "us-east-1"
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgent-EqFCwr3WrQ"

def force_update_runtime():
    """Force update the AgentCore runtime"""
    
    print("🔄 Force Updating AgentCore Runtime")
    print("=" * 40)
    
    # Initialize clients
    session = boto3.Session(profile_name=AWS_PROFILE)
    sts_client = session.client('sts')
    agentcore_client = session.client('bedrock-agentcore', region_name=AWS_REGION)
    
    # Get account ID
    account_id = sts_client.get_caller_identity()['Account']
    
    # Container configuration
    container_uri = f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/helloworld-strands-agent:latest"
    role_arn = f"arn:aws:iam::{account_id}:role/AgentRuntimeRole"
    
    print(f"📦 Container: {container_uri}")
    print(f"🔑 Role: {role_arn}")
    
    try:
        # Update the runtime with environment variables
        print("🚀 Updating runtime...")
        
        update_response = agentcore_client.update_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            containerConfiguration={
                'containerUri': container_uri,
                'executionRoleArn': role_arn,
                'environmentVariables': {
                    'AWS_PROFILE': AWS_PROFILE,
                    'AWS_REGION': AWS_REGION,
                    'TAVILY_API_KEY': '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'
                }
            }
        )
        
        print("✅ Update initiated!")
        print(f"📋 ARN: {update_response['agentRuntimeArn']}")
        
        # Wait a bit for update to process
        print("⏳ Waiting 30 seconds for update...")
        time.sleep(30)
        
        # Test the updated runtime
        test_response = agentcore_client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId="update-test-session-12345678901234567890123456789012",
            payload=json.dumps({
                'prompt': 'Search for the latest news about AWS Bedrock',
                'session_id': 'update-test-session',
                'memory_id': 'update-test-memory'
            })
        )
        
        result = json.loads(test_response['response'].read())
        
        if result['status'] == 'success':
            print("🎉 Runtime updated and tested successfully!")
            response_text = result['response']['content'][0]['text']
            has_search = any(word in response_text.lower() for word in ['search', 'latest', 'recent', 'according'])
            print(f"🔍 Search capability: {'✅ Working' if has_search else '❌ Not detected'}")
            return True
        else:
            print(f"❌ Test failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Update failed: {e}")
        return False

if __name__ == "__main__":
    success = force_update_runtime()
    print(f"\n📋 Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"🚀 Runtime ARN: {AGENT_RUNTIME_ARN}")
