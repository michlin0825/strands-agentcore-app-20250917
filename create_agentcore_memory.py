#!/usr/bin/env python3
"""
Create explicit AgentCore Memory resource
"""

import boto3
import json
from datetime import datetime, timedelta

# Configuration
AWS_PROFILE = "CloudChef01"
AWS_REGION = "us-east-1"
MEMORY_ID = "helloworldmemory"  # No hyphens allowed

def create_agentcore_memory():
    """Create explicit AgentCore Memory resource"""
    
    print("🧠 Creating AgentCore Memory Resource")
    print("=" * 40)
    
    session = boto3.Session(profile_name=AWS_PROFILE)
    client = session.client('bedrock-agentcore-control', region_name=AWS_REGION)
    
    try:
        # Check if memory already exists
        print("🔍 Checking existing memories...")
        existing_memories = client.list_memories()
        
        memory_exists = False
        for memory in existing_memories.get('memories', []):
            if memory.get('name') == MEMORY_ID:
                memory_exists = True
                print(f"✅ Memory '{MEMORY_ID}' already exists")
                break
        
        if not memory_exists:
            print(f"📝 Creating memory '{MEMORY_ID}'...")
            
            # Create memory with 30-day retention
            expiration_time = datetime.now() + timedelta(days=30)
            
            response = client.create_memory(
                name=MEMORY_ID,
                description="HelloWorld Strands Agent conversation memory",
                eventExpiryDuration=30  # 30 days as integer
            )
            
            print("✅ Memory created successfully!")
            print(f"📋 Memory Name: {response.get('name')}")
            print(f"📋 Memory ARN: {response.get('memoryArn', 'N/A')}")
        
        # List all memories
        print("\n📋 All AgentCore Memories:")
        memories = client.list_memories()
        
        if memories.get('memories'):
            for memory in memories['memories']:
                print(f"  - Name: {memory.get('name')}")
                print(f"    ARN: {memory.get('memoryArn', 'N/A')}")
                print(f"    Status: {memory.get('status', 'N/A')}")
                print(f"    Created: {memory.get('createdAt', 'N/A')}")
                print()
        else:
            print("  No memories found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating memory: {e}")
        return False

def test_memory_functionality():
    """Test the memory functionality"""
    print("\n🧪 Testing Memory Functionality")
    print("=" * 30)
    
    session = boto3.Session(profile_name=AWS_PROFILE)
    agentcore_client = session.client('bedrock-agentcore', region_name=AWS_REGION)
    
    try:
        # Test memory storage
        session_id = "memory-creation-test-12345678901234567890123456789012"
        
        response = agentcore_client.invoke_agent_runtime(
            agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgent-EqFCwr3WrQ',
            runtimeSessionId=session_id,
            payload=json.dumps({
                'prompt': 'Remember: I am testing the explicit memory creation',
                'session_id': session_id,
                'memory_id': MEMORY_ID
            })
        )
        
        result = json.loads(response['response'].read())
        
        if result['status'] == 'success':
            print("✅ Memory test successful!")
            response_text = result['response']['content'][0]['text']
            print(f"📝 Response: {response_text[:150]}...")
            return True
        else:
            print(f"❌ Memory test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Memory test error: {e}")
        return False

if __name__ == "__main__":
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create memory
    memory_created = create_agentcore_memory()
    
    if memory_created:
        # Test functionality
        test_memory_functionality()
    
    print(f"\n📋 Summary:")
    print(f"   Memory ID: {MEMORY_ID}")
    print(f"   Region: {AWS_REGION}")
    print(f"   Profile: {AWS_PROFILE}")
    print(f"   Console: AWS Console → Bedrock AgentCore → Memory")
