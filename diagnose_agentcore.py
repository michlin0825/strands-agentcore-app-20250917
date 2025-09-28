#!/usr/bin/env python3
"""
Comprehensive AgentCore Diagnostic Tool
"""

import boto3
import json
import time
from datetime import datetime, timedelta

AWS_PROFILE = "CloudChef01"
AWS_REGION = "us-east-1"
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgent-EqFCwr3WrQ"

def diagnose_agentcore():
    """Comprehensive diagnostic of AgentCore components"""
    
    print("🔍 AgentCore Comprehensive Diagnostics")
    print("=" * 50)
    
    session = boto3.Session(profile_name=AWS_PROFILE)
    
    # 1. Check ECR Repository
    print("\n1️⃣ ECR Repository Status")
    print("-" * 25)
    try:
        ecr_client = session.client('ecr', region_name=AWS_REGION)
        images = ecr_client.describe_images(
            repositoryName='helloworld-strands-agent',
            maxResults=5
        )
        
        print(f"✅ ECR Repository exists")
        print(f"📦 Images found: {len(images['imageDetails'])}")
        
        for img in images['imageDetails'][:3]:
            tags = img.get('imageTags', ['<untagged>'])
            pushed = img['imagePushedAt'].strftime('%Y-%m-%d %H:%M:%S')
            size_mb = img['imageSizeInBytes'] / (1024*1024)
            print(f"   - Tags: {tags}, Size: {size_mb:.1f}MB, Pushed: {pushed}")
            
    except Exception as e:
        print(f"❌ ECR Error: {e}")
    
    # 2. Check Memory Resource
    print("\n2️⃣ AgentCore Memory Status")
    print("-" * 28)
    try:
        control_client = session.client('bedrock-agentcore-control', region_name=AWS_REGION)
        memories = control_client.list_memories()
        
        print(f"✅ Memory service accessible")
        print(f"🧠 Memories found: {len(memories.get('memories', []))}")
        
        for memory in memories.get('memories', []):
            name = memory.get('name', 'Unknown')
            status = memory.get('status', 'Unknown')
            created = memory.get('createdAt', 'Unknown')
            print(f"   - Name: {name}, Status: {status}, Created: {created}")
            
    except Exception as e:
        print(f"❌ Memory Error: {e}")
    
    # 3. Check IAM Role
    print("\n3️⃣ IAM Role Status")
    print("-" * 18)
    try:
        iam_client = session.client('iam', region_name=AWS_REGION)
        role = iam_client.get_role(RoleName='AgentRuntimeRole')
        
        print(f"✅ AgentRuntimeRole exists")
        print(f"📋 Created: {role['Role']['CreateDate']}")
        
        # Check attached policies
        policies = iam_client.list_attached_role_policies(RoleName='AgentRuntimeRole')
        print(f"🔐 Attached policies: {len(policies['AttachedPolicies'])}")
        
        for policy in policies['AttachedPolicies']:
            print(f"   - {policy['PolicyName']}")
            
    except Exception as e:
        print(f"❌ IAM Error: {e}")
    
    # 4. Check CloudWatch Logs
    print("\n4️⃣ CloudWatch Logs Analysis")
    print("-" * 29)
    try:
        logs_client = session.client('logs', region_name=AWS_REGION)
        
        # Get log groups
        log_groups = logs_client.describe_log_groups(
            logGroupNamePrefix='/aws/bedrock-agentcore'
        )
        
        print(f"✅ Found {len(log_groups['logGroups'])} AgentCore log groups")
        
        for lg in log_groups['logGroups']:
            group_name = lg['logGroupName']
            print(f"📋 Log Group: {group_name}")
            
            # Get recent log streams
            try:
                streams = logs_client.describe_log_streams(
                    logGroupName=group_name,
                    orderBy='LastEventTime',
                    descending=True,
                    limit=3
                )
                
                print(f"   📊 Recent streams: {len(streams['logStreams'])}")
                
                for stream in streams['logStreams'][:2]:
                    stream_name = stream['logStreamName']
                    last_event = stream.get('lastEventTimestamp')
                    
                    if last_event:
                        last_time = datetime.fromtimestamp(last_event/1000)
                        print(f"   - {stream_name}: {last_time}")
                        
                        # Get recent log events
                        try:
                            events = logs_client.get_log_events(
                                logGroupName=group_name,
                                logStreamName=stream_name,
                                limit=5,
                                startFromHead=False
                            )
                            
                            print(f"     📝 Recent events: {len(events['events'])}")
                            for event in events['events'][-2:]:
                                timestamp = datetime.fromtimestamp(event['timestamp']/1000)
                                message = event['message'][:100]
                                print(f"     {timestamp}: {message}...")
                                
                        except Exception as e:
                            print(f"     ❌ Events error: {e}")
                            
            except Exception as e:
                print(f"   ❌ Streams error: {e}")
                
    except Exception as e:
        print(f"❌ CloudWatch Error: {e}")
    
    # 5. Test AgentCore Runtime
    print("\n5️⃣ AgentCore Runtime Test")
    print("-" * 26)
    try:
        agentcore_client = session.client('bedrock-agentcore', region_name=AWS_REGION)
        
        test_payload = {
            'prompt': 'Simple test message',
            'session_id': 'diagnostic-test',
            'memory_id': 'helloworld-memory'
        }
        
        print("🧪 Attempting runtime invocation...")
        response = agentcore_client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId='diagnostic-test-session-12345678901234567890123456789012',
            payload=json.dumps(test_payload)
        )
        
        result = json.loads(response['response'].read())
        print(f"✅ Runtime responded: {result.get('status', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Runtime Error: {e}")
        error_str = str(e)
        
        if "RuntimeClientError" in error_str:
            print("🔍 Analysis: Container startup failure")
            print("   Possible causes:")
            print("   - Code syntax errors")
            print("   - Missing dependencies")
            print("   - Memory/resource limits")
            print("   - Environment variable issues")
        elif "ValidationException" in error_str:
            print("🔍 Analysis: Request validation failure")
        elif "AccessDenied" in error_str:
            print("🔍 Analysis: IAM permission issues")
        else:
            print(f"🔍 Analysis: Unknown error pattern")
    
    # 6. Recommendations
    print("\n6️⃣ Diagnostic Summary & Recommendations")
    print("-" * 42)
    
    recommendations = []
    
    # Check if we should recreate runtime
    print("🎯 Recovery Options:")
    print("   A) Fix container code issues")
    print("   B) Recreate AgentCore Runtime")
    print("   C) Revert to last working container")
    print("   D) Create new runtime with fresh configuration")
    
    return True

if __name__ == "__main__":
    diagnose_agentcore()
