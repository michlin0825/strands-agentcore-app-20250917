#!/usr/bin/env python3
"""
Update AgentCore Runtime using AWS CLI
"""

import subprocess
import json
import time

# Configuration
AWS_PROFILE = "CloudChef01"
AWS_REGION = "us-east-1"
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgent-EqFCwr3WrQ"

def get_runtime_id_from_arn(arn):
    """Extract runtime ID from ARN"""
    return arn.split('/')[-1]

def update_runtime_with_cli():
    """Update AgentCore runtime using AWS CLI"""
    
    print("🔄 Updating AgentCore Runtime with AWS CLI")
    print("=" * 50)
    
    # Extract runtime ID from ARN
    runtime_id = get_runtime_id_from_arn(AGENT_RUNTIME_ARN)
    print(f"📋 Runtime ID: {runtime_id}")
    
    # Get account ID
    try:
        result = subprocess.run([
            'aws', 'sts', 'get-caller-identity',
            '--profile', AWS_PROFILE,
            '--region', AWS_REGION,
            '--output', 'json'
        ], capture_output=True, text=True, check=True)
        
        account_info = json.loads(result.stdout)
        account_id = account_info['Account']
        print(f"📋 Account ID: {account_id}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get account ID: {e}")
        return False
    
    # Container configuration
    container_uri = f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/helloworld-strands-agent:latest"
    role_arn = f"arn:aws:iam::{account_id}:role/AgentRuntimeRole"
    
    print(f"📦 Container: {container_uri}")
    print(f"🔑 Role: {role_arn}")
    
    # Prepare update command
    update_cmd = [
        'aws', 'bedrock-agentcore-control', 'update-agent-runtime',
        '--agent-runtime-id', runtime_id,
        '--agent-runtime-artifact', json.dumps({
            'containerArtifact': {
                'containerUri': container_uri
            }
        }),
        '--role-arn', role_arn,
        '--network-configuration', json.dumps({
            'vpcConfiguration': {
                'subnetIds': [],
                'securityGroupIds': []
            }
        }),
        '--environment-variables', json.dumps({
            'AWS_PROFILE': AWS_PROFILE,
            'AWS_REGION': AWS_REGION,
            'TAVILY_API_KEY': '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'
        }),
        '--profile', AWS_PROFILE,
        '--region', AWS_REGION,
        '--output', 'json'
    ]
    
    try:
        print("🚀 Executing update command...")
        result = subprocess.run(update_cmd, capture_output=True, text=True, check=True)
        
        update_response = json.loads(result.stdout)
        print("✅ Update command executed successfully!")
        print(f"📋 Response: {json.dumps(update_response, indent=2)}")
        
        # Wait for update to process
        print("⏳ Waiting 60 seconds for update to complete...")
        time.sleep(60)
        
        # Test the updated runtime
        return test_updated_runtime()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Update failed: {e}")
        print(f"❌ Error output: {e.stderr}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse response: {e}")
        return False

def test_updated_runtime():
    """Test the updated runtime"""
    print("\n🧪 Testing Updated Runtime")
    print("=" * 30)
    
    import boto3
    
    try:
        session = boto3.Session(profile_name=AWS_PROFILE)
        client = session.client('bedrock-agentcore', region_name=AWS_REGION)
        
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId="cli-update-test-session-12345678901234567890123456789012",
            payload=json.dumps({
                'prompt': 'Search for the latest AWS announcements',
                'session_id': 'cli-update-test',
                'memory_id': 'cli-update-memory'
            })
        )
        
        result = json.loads(response['response'].read())
        
        if result['status'] == 'success':
            response_text = result['response']['content'][0]['text']
            has_search = any(word in response_text.lower() for word in ['search', 'latest', 'recent'])
            
            print("✅ Runtime test successful!")
            print(f"🔍 Search capability: {'✅ Working' if has_search else '❌ Not detected'}")
            print(f"📝 Response preview: {response_text[:150]}...")
            return True
        else:
            print(f"❌ Test failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = update_runtime_with_cli()
    print(f"\n📋 Final Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"🚀 Runtime ARN: {AGENT_RUNTIME_ARN}")
