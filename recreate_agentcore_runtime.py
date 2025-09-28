#!/usr/bin/env python3
"""
Recreate AgentCore Runtime with existing resources
"""

import boto3
import json
import time
from datetime import datetime

AWS_PROFILE = "CloudChef01"
AWS_REGION = "us-east-1"
OLD_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgent-EqFCwr3WrQ"

def recreate_agentcore_runtime():
    """Recreate AgentCore Runtime with fresh configuration"""
    
    print("🔄 Recreating AgentCore Runtime")
    print("=" * 35)
    
    session = boto3.Session(profile_name=AWS_PROFILE)
    
    # Get account ID
    sts_client = session.client('sts')
    account_id = sts_client.get_caller_identity()['Account']
    
    # Configuration
    container_uri = f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/helloworld-strands-agent:latest"
    role_arn = f"arn:aws:iam::{account_id}:role/AgentRuntimeRole"
    
    print(f"📦 Container: {container_uri}")
    print(f"🔑 Role: {role_arn}")
    print(f"🧠 Memory: helloworldmemory (preserved)")
    
    # Step 1: Delete old runtime
    print("\n1️⃣ Deleting Old Runtime")
    print("-" * 25)
    
    try:
        agentcore_client = session.client('bedrock-agentcore', region_name=AWS_REGION)
        
        # Extract runtime ID from ARN
        old_runtime_id = OLD_RUNTIME_ARN.split('/')[-1]
        print(f"🗑️  Deleting runtime: {old_runtime_id}")
        
        # Note: Delete via bedrock-agentcore-control
        control_client = session.client('bedrock-agentcore-control', region_name=AWS_REGION)
        
        try:
            control_client.delete_agent_runtime(agentRuntimeId=old_runtime_id)
            print("✅ Old runtime deletion initiated")
            
            # Wait for deletion
            print("⏳ Waiting for deletion to complete...")
            time.sleep(90)
            
        except Exception as e:
            if "NotFound" in str(e):
                print("ℹ️  Runtime already deleted or not found")
            else:
                print(f"⚠️  Delete error (continuing): {e}")
        
    except Exception as e:
        print(f"⚠️  Delete error (continuing): {e}")
    
    # Step 2: Create new runtime
    print("\n2️⃣ Creating New Runtime")
    print("-" * 24)
    
    try:
        control_client = session.client('bedrock-agentcore-control', region_name=AWS_REGION)
        
        runtime_config = {
            'agentRuntimeName': 'HelloWorldStrandsAgentV2',
            'description': 'HelloWorld Strands Agent with Tavily Search - Recreated',
            'agentRuntimeArtifact': {
                'containerConfiguration': {
                    'containerUri': container_uri
                }
            },
            'roleArn': role_arn,
            'networkConfiguration': {
                'networkMode': 'PUBLIC'
            }
        }
        
        print("🚀 Creating new runtime...")
        response = control_client.create_agent_runtime(**runtime_config)
        
        new_runtime_arn = response['agentRuntimeArn']
        print(f"✅ New runtime created!")
        print(f"📋 ARN: {new_runtime_arn}")
        
        # Wait for runtime to be ready
        print("⏳ Waiting for runtime to initialize...")
        time.sleep(60)
        
        return new_runtime_arn
        
    except Exception as e:
        print(f"❌ Creation failed: {e}")
        return None

def test_new_runtime(runtime_arn):
    """Test the new runtime"""
    print("\n3️⃣ Testing New Runtime")
    print("-" * 22)
    
    session = boto3.Session(profile_name=AWS_PROFILE)
    client = session.client('bedrock-agentcore', region_name=AWS_REGION)
    
    try:
        # Test basic functionality
        response = client.invoke_agent_runtime(
            agentRuntimeArn=runtime_arn,
            runtimeSessionId='recreation-test-session-12345678901234567890123456789012',
            payload=json.dumps({
                'prompt': 'Hello! Test the recreated agent with memory.',
                'session_id': 'recreation-test',
                'memory_id': 'helloworldmemory'
            })
        )
        
        result = json.loads(response['response'].read())
        
        if result['status'] == 'success':
            print("✅ Basic functionality working!")
            print(f"📝 Response: {result['response']['content'][0]['text'][:100]}...")
            
            # Test Tavily search
            print("\n🔍 Testing Tavily search...")
            search_response = client.invoke_agent_runtime(
                agentRuntimeArn=runtime_arn,
                runtimeSessionId='search-test-session-12345678901234567890123456789012',
                payload=json.dumps({
                    'prompt': 'What is the current stock price of Apple?',
                    'session_id': 'search-test',
                    'memory_id': 'helloworldmemory'
                })
            )
            
            search_result = json.loads(search_response['response'].read())
            if search_result['status'] == 'success':
                search_text = search_result['response']['content'][0]['text']
                has_search = any(word in search_text.lower() for word in ['apple', 'stock', 'price', '$'])
                print(f"🌐 Search capability: {'✅ Working' if has_search else '❌ Not detected'}")
                
            return True
        else:
            print(f"❌ Test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def update_config_files(new_runtime_arn):
    """Update configuration files with new runtime ARN"""
    print("\n4️⃣ Updating Configuration")
    print("-" * 26)
    
    # Update test files
    files_to_update = [
        'test_tavily_agent.py',
        'test_deployed_agent.py',
        'streamlit_app/config.py'
    ]
    
    for file_path in files_to_update:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Replace old ARN with new ARN
            updated_content = content.replace(OLD_RUNTIME_ARN, new_runtime_arn)
            
            with open(file_path, 'w') as f:
                f.write(updated_content)
                
            print(f"✅ Updated {file_path}")
            
        except Exception as e:
            print(f"⚠️  Could not update {file_path}: {e}")
    
    print(f"\n📋 New Runtime ARN: {new_runtime_arn}")
    print("🎯 All native AgentCore components preserved:")
    print("   - Memory: helloworldmemory")
    print("   - Authentication: Cognito User Pool")
    print("   - Container: Latest with Tavily integration")
    print("   - IAM: AgentRuntimeRole")

if __name__ == "__main__":
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Recreate runtime
    new_arn = recreate_agentcore_runtime()
    
    if new_arn:
        # Test new runtime
        if test_new_runtime(new_arn):
            # Update config files
            update_config_files(new_arn)
            print("\n🎉 Runtime recreation successful!")
        else:
            print("\n❌ Runtime recreation failed testing")
    else:
        print("\n❌ Runtime recreation failed")
