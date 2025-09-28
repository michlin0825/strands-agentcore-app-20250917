#!/usr/bin/env python3
"""
Update existing AgentCore Runtime with new container image
"""

import boto3
import json
import time
from datetime import datetime

# Configuration
AWS_PROFILE = "CloudChef01"
AWS_REGION = "us-east-1"
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgent-EqFCwr3WrQ"

def update_agent_runtime():
    """Update the existing AgentCore runtime with new container"""
    
    print("🔄 Updating AgentCore Runtime with Tavily Search")
    print("=" * 50)
    
    # Initialize clients
    session = boto3.Session(profile_name=AWS_PROFILE)
    sts_client = session.client('sts')
    ecr_client = session.client('ecr', region_name=AWS_REGION)
    agentcore_client = session.client('bedrock-agentcore', region_name=AWS_REGION)
    
    # Get account ID
    account_id = sts_client.get_caller_identity()['Account']
    print(f"📋 Account ID: {account_id}")
    
    # Container configuration
    container_uri = f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/helloworld-strands-agent:latest"
    role_arn = f"arn:aws:iam::{account_id}:role/AgentRuntimeRole"
    
    print(f"📦 Container URI: {container_uri}")
    print(f"🔑 Role ARN: {role_arn}")
    
    try:
        # Check if image exists in ECR
        print("🔍 Checking ECR image...")
        try:
            ecr_client.describe_images(
                repositoryName='helloworld-strands-agent',
                imageIds=[{'imageTag': 'latest'}]
            )
            print("✅ ECR image found")
        except ecr_client.exceptions.ImageNotFoundException:
            print("❌ ECR image not found. Please build and push the image first.")
            return False
        
        # Get current runtime details
        print("🔍 Getting current runtime details...")
        current_runtime = agentcore_client.describe_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN
        )
        
        current_config = current_runtime['agentRuntime']
        print(f"📋 Current Runtime: {current_config['agentRuntimeName']}")
        print(f"📋 Current Status: {current_config['agentRuntimeStatus']}")
        
        # Update the runtime
        print("🔄 Updating AgentCore Runtime...")
        
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
        
        print("✅ Update initiated successfully!")
        print(f"📋 Update ARN: {update_response['agentRuntimeArn']}")
        
        # Wait for update to complete
        print("⏳ Waiting for update to complete...")
        max_wait = 300  # 5 minutes
        wait_time = 0
        
        while wait_time < max_wait:
            try:
                runtime_status = agentcore_client.describe_agent_runtime(
                    agentRuntimeArn=AGENT_RUNTIME_ARN
                )
                
                status = runtime_status['agentRuntime']['agentRuntimeStatus']
                print(f"📊 Status: {status}")
                
                if status == 'ACTIVE':
                    print("🎉 AgentCore Runtime updated successfully!")
                    print(f"🚀 Runtime ARN: {AGENT_RUNTIME_ARN}")
                    return True
                elif status in ['FAILED', 'STOPPED']:
                    print(f"❌ Update failed with status: {status}")
                    return False
                
                time.sleep(10)
                wait_time += 10
                
            except Exception as e:
                print(f"⚠️  Error checking status: {e}")
                time.sleep(5)
                wait_time += 5
        
        print("⏰ Update timeout - check AWS console for status")
        return False
        
    except Exception as e:
        print(f"❌ Update failed: {e}")
        return False

def test_updated_agent():
    """Test the updated agent with Tavily search"""
    print("\n🧪 Testing Updated Agent")
    print("=" * 30)
    
    session = boto3.Session(profile_name=AWS_PROFILE)
    client = session.client('bedrock-agentcore', region_name=AWS_REGION)
    
    test_prompt = "Search for the latest news about AWS re:Invent 2024"
    session_id = f"update-test-{int(time.time())}-session-long-enough"
    
    try:
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId=session_id,
            payload=json.dumps({
                'prompt': test_prompt,
                'session_id': session_id,
                'memory_id': 'update-test-memory'
            })
        )
        
        result = json.loads(response['response'].read())
        
        if result['status'] == 'success':
            response_text = result['response']['content'][0]['text']
            print("✅ Test successful!")
            print(f"🔍 Response includes search: {'search' in response_text.lower()}")
            print(f"📝 Response preview: {response_text[:150]}...")
            return True
        else:
            print(f"❌ Test failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Update the runtime
    if update_agent_runtime():
        # Test the updated agent
        time.sleep(5)  # Give it a moment
        test_updated_agent()
    
    print(f"\n📋 Summary:")
    print(f"   Runtime ARN: {AGENT_RUNTIME_ARN}")
    print(f"   Profile: {AWS_PROFILE}")
    print(f"   Region: {AWS_REGION}")
