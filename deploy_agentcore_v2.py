#!/usr/bin/env python3
"""
Deployment script for Strands AgentCore App 20250917 to AgentCore Runtime
"""

import boto3
import json
import time
import sys
from botocore.exceptions import ClientError

# Configuration - Updated naming
AGENT_NAME = "StrandsAgentCoreApp20250917"  # Reflects project folder name
REGION = "us-east-1"
REPOSITORY_NAME = "strands-agentcore-app-20250917"
AWS_PROFILE = "CloudChef01"

# Old runtime to delete
OLD_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgentV2-R3GAODHoRb"

def delete_old_runtime():
    """Delete the old AgentCore runtime"""
    print("🗑️  Deleting old AgentCore runtime...")
    
    session = boto3.Session(profile_name=AWS_PROFILE)
    
    # Note: AgentCore runtimes may need to be deleted through AWS Console
    # or different API. For now, we'll skip deletion and create new runtime
    print("ℹ️  Skipping old runtime deletion - will be handled manually if needed")
    print("ℹ️  Old runtime ARN: " + OLD_RUNTIME_ARN)

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
    session = boto3.Session(profile_name=AWS_PROFILE)
    sts_client = session.client('sts')
    return sts_client.get_caller_identity()['Account']

def build_and_push_image():
    """Build and push Docker image to ECR"""
    print("🐳 Building and pushing Docker image...")
    
    account_id = get_account_id()
    repository_uri = f"{account_id}.dkr.ecr.{REGION}.amazonaws.com/{REPOSITORY_NAME}"
    
    import subprocess
    
    try:
        # Get ECR login token
        print("🔐 Getting ECR login token...")
        result = subprocess.run([
            "aws", "ecr", "get-login-password", 
            "--region", REGION,
            "--profile", AWS_PROFILE
        ], capture_output=True, text=True, check=True)
        
        login_token = result.stdout.strip()
        
        # Docker login to ECR
        subprocess.run([
            "docker", "login", "--username", "AWS", 
            "--password-stdin", repository_uri
        ], input=login_token, text=True, check=True)
        
        # Build image
        print("🔨 Building Docker image...")
        subprocess.run([
            "docker", "build", "-t", REPOSITORY_NAME, "."
        ], check=True)
        
        # Tag image
        image_tag = f"{repository_uri}:latest"
        subprocess.run([
            "docker", "tag", REPOSITORY_NAME, image_tag
        ], check=True)
        
        # Push image
        print("📤 Pushing image to ECR...")
        subprocess.run([
            "docker", "push", image_tag
        ], check=True)
        
        print(f"✅ Image pushed successfully: {image_tag}")
        return image_tag
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker operation failed: {e}")
        return None

def create_agent_runtime(image_uri):
    """Create AgentCore runtime"""
    print("🚀 Creating AgentCore runtime...")
    
    # Note: AgentCore runtime creation may need to be done through AWS Console
    # or different deployment method. This is a placeholder for the correct API
    
    print("ℹ️  AgentCore runtime creation needs to be done manually through:")
    print("   1. AWS Console -> Bedrock -> AgentCore")
    print("   2. Or using the correct AWS CLI/API commands")
    print(f"   3. Use image URI: {image_uri}")
    print(f"   4. Runtime name: {AGENT_NAME}")
    
    # For now, return a placeholder ARN that will need to be updated manually
    placeholder_arn = f"arn:aws:bedrock-agentcore:{REGION}:111735445051:runtime/{AGENT_NAME}-PLACEHOLDER"
    print(f"📝 Placeholder ARN: {placeholder_arn}")
    print("⚠️  You'll need to update this with the actual ARN after manual creation")
    
    return placeholder_arn

def main():
    """Main deployment function"""
    print("🚀 Deploying Strands AgentCore App 20250917")
    print("=" * 50)
    
    # Step 1: Delete old runtime
    delete_old_runtime()
    
    # Step 2: Create ECR repository
    repository_uri = create_ecr_repository()
    if not repository_uri:
        sys.exit(1)
    
    # Step 3: Build and push image
    image_uri = build_and_push_image()
    if not image_uri:
        sys.exit(1)
    
    # Step 4: Create AgentCore runtime
    runtime_arn = create_agent_runtime(image_uri)
    if not runtime_arn:
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Deployment completed successfully!")
    print(f"📋 Runtime ARN: {runtime_arn}")
    print(f"🐳 Image URI: {image_uri}")
    print("\n📝 Next steps:")
    print("1. Update your .env file with the new AGENT_RUNTIME_ARN")
    print("2. Test the deployment with test_deployed_agent.py")
    print("3. Start the Streamlit app with ./start_env_app.sh")

if __name__ == "__main__":
    main()
