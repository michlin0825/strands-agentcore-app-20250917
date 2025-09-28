#!/usr/bin/env python3
"""
Deployment script for HelloWorld Strands Agent to AgentCore Runtime
"""

import boto3
import json
import time
import sys
from botocore.exceptions import ClientError

# Configuration
AGENT_NAME = "HelloWorldStrandsAgent"  # Fixed: no hyphens allowed
REGION = "us-east-1"  # CloudChef01 profile region
REPOSITORY_NAME = "helloworld-strands-agent"
AWS_PROFILE = "CloudChef01"

def create_ecr_repository():
    """Create ECR repository if it doesn't exist"""
    print("🔍 Checking ECR repository...")
    
    session = boto3.Session(profile_name=AWS_PROFILE)
    ecr_client = session.client('ecr', region_name=REGION)
    
    try:
        # Check if repository exists
        response = ecr_client.describe_repositories(repositoryNames=[REPOSITORY_NAME])
        print(f"✅ ECR repository '{REPOSITORY_NAME}' already exists")
        return response['repositories'][0]['repositoryUri']
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'RepositoryNotFoundException':
            print(f"📦 Creating ECR repository '{REPOSITORY_NAME}'...")
            try:
                response = ecr_client.create_repository(
                    repositoryName=REPOSITORY_NAME,
                    imageScanningConfiguration={'scanOnPush': True}
                )
                repository_uri = response['repository']['repositoryUri']
                print(f"✅ ECR repository created: {repository_uri}")
                return repository_uri
                
            except ClientError as create_error:
                print(f"❌ Failed to create ECR repository: {create_error}")
                return None
        else:
            print(f"❌ Error checking ECR repository: {e}")
            return None

def get_account_id():
    """Get AWS account ID"""
    try:
        session = boto3.Session(profile_name=AWS_PROFILE)
        sts_client = session.client('sts')
        response = sts_client.get_caller_identity()
        return response['Account']
    except Exception as e:
        print(f"❌ Failed to get account ID: {e}")
        return None

def create_agent_runtime(container_uri, role_arn):
    """Create AgentCore Runtime"""
    print("🚀 Creating AgentCore Runtime...")
    
    try:
        session = boto3.Session(profile_name=AWS_PROFILE)
        client = session.client('bedrock-agentcore-control', region_name=REGION)
        
        response = client.create_agent_runtime(
            agentRuntimeName=AGENT_NAME,
            agentRuntimeArtifact={
                'containerConfiguration': {
                    'containerUri': container_uri
                }
            },
            networkConfiguration={"networkMode": "PUBLIC"},
            roleArn=role_arn
        )
        
        print(f"✅ AgentCore Runtime created successfully!")
        print(f"   Runtime ARN: {response['agentRuntimeArn']}")
        print(f"   Status: {response['status']}")
        
        return response['agentRuntimeArn']
        
    except ClientError as e:
        print(f"❌ Failed to create AgentCore Runtime: {e}")
        return None

def wait_for_runtime_ready(runtime_arn):
    """Wait for runtime to be ready"""
    print("⏳ Waiting for runtime to be ready...")
    
    session = boto3.Session(profile_name=AWS_PROFILE)
    client = session.client('bedrock-agentcore-control', region_name=REGION)
    
    for i in range(30):  # Wait up to 15 minutes
        try:
            response = client.get_agent_runtime(agentRuntimeArn=runtime_arn)
            status = response['status']
            
            print(f"   Status: {status}")
            
            if status == 'ACTIVE':
                print("✅ Runtime is ready!")
                return True
            elif status in ['FAILED', 'STOPPED']:
                print(f"❌ Runtime failed with status: {status}")
                return False
            
            time.sleep(30)  # Wait 30 seconds
            
        except ClientError as e:
            print(f"❌ Error checking runtime status: {e}")
            return False
    
    print("❌ Timeout waiting for runtime to be ready")
    return False

def test_agent_runtime(runtime_arn):
    """Test the deployed agent"""
    print("🧪 Testing deployed agent...")
    
    try:
        session = boto3.Session(profile_name=AWS_PROFILE)
        client = session.client('bedrock-agentcore', region_name=REGION)
        
        payload = json.dumps({
            "prompt": "Hello! This is a test from the deployment script."
        })
        
        response = client.invoke_agent_runtime(
            agentRuntimeArn=runtime_arn,
            runtimeSessionId="deployment-test-session-12345678901234567890123456789012",  # Must be 33+ chars
            payload=payload
        )
        
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        
        if response_data.get('status') == 'success':
            print("✅ Agent test successful!")
            print(f"   Response: {response_data.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ Agent test failed: {response_data}")
            return False
            
    except Exception as e:
        print(f"❌ Agent test error: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 HelloWorld Strands Agent - AgentCore Deployment")
    print("=" * 60)
    
    # Get account ID
    account_id = get_account_id()
    if not account_id:
        sys.exit(1)
    
    print(f"📋 Account ID: {account_id}")
    print(f"📋 Region: {REGION}")
    
    # Create ECR repository
    repository_uri = create_ecr_repository()
    if not repository_uri:
        sys.exit(1)
    
    # Construct container URI
    container_uri = f"{repository_uri}:latest"
    
    # Construct role ARN (you may need to adjust this)
    role_arn = f"arn:aws:iam::{account_id}:role/AgentRuntimeRole"
    
    print(f"\n📋 Configuration:")
    print(f"   Container URI: {container_uri}")
    print(f"   Role ARN: {role_arn}")
    
    # Instructions for building and pushing image
    print(f"\n📦 Next Steps - Build and Push Docker Image:")
    print(f"   1. Build the image:")
    print(f"      docker buildx build --platform linux/arm64 -t {AGENT_NAME} .")
    print(f"   ")
    print(f"   2. Login to ECR:")
    print(f"      aws ecr get-login-password --region {REGION} --profile {AWS_PROFILE} | docker login --username AWS --password-stdin {account_id}.dkr.ecr.{REGION}.amazonaws.com")
    print(f"   ")
    print(f"   3. Tag and push:")
    print(f"      docker tag {AGENT_NAME}:latest {container_uri}")
    print(f"      docker push {container_uri}")
    print(f"   ")
    print(f"   4. Run this script again to deploy to AgentCore")
    
    # Check if image exists in ECR
    print(f"\n🔍 Checking if Docker image exists in ECR...")
    session = boto3.Session(profile_name=AWS_PROFILE)
    ecr_client = session.client('ecr', region_name=REGION)
    
    try:
        response = ecr_client.describe_images(
            repositoryName=REPOSITORY_NAME,
            imageIds=[{'imageTag': 'latest'}]
        )
        
        if response['imageDetails']:
            print("✅ Docker image found in ECR, proceeding with deployment...")
            
            # Create AgentCore Runtime
            runtime_arn = create_agent_runtime(container_uri, role_arn)
            if not runtime_arn:
                sys.exit(1)
            
            # Wait for runtime to be ready
            if wait_for_runtime_ready(runtime_arn):
                # Test the agent
                test_agent_runtime(runtime_arn)
                
                print(f"\n🎉 Deployment Complete!")
                print(f"   Runtime ARN: {runtime_arn}")
                print(f"   ")
                print(f"   Test your agent with:")
                print(f"   agentcore invoke '{{\"prompt\": \"Hello from AgentCore!\"}}'")
            
        else:
            print("❌ No Docker image found in ECR")
            print("   Please build and push the Docker image first (see instructions above)")
            
    except ClientError as e:
        if e.response['Error']['Code'] == 'ImageNotFoundException':
            print("❌ Docker image not found in ECR")
            print("   Please build and push the Docker image first (see instructions above)")
        else:
            print(f"❌ Error checking ECR image: {e}")

if __name__ == "__main__":
    main()
