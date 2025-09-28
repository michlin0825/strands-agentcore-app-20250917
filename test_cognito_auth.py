#!/usr/bin/env python3
"""
Test Cognito authentication for AgentCore identity
"""

import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cognito Configuration from environment
USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
USERNAME = os.getenv('COGNITO_USERNAME')
PASSWORD = os.getenv('COGNITO_PASSWORD')
REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_PROFILE = os.getenv('AWS_PROFILE', 'default')

# Validate required environment variables
if not all([USER_POOL_ID, CLIENT_ID, USERNAME, PASSWORD]):
    print("❌ Error: Missing required Cognito environment variables")
    print("Please check your .env file for:")
    print("- COGNITO_USER_POOL_ID")
    print("- COGNITO_CLIENT_ID") 
    print("- COGNITO_USERNAME")
    print("- COGNITO_PASSWORD")
    exit(1)

def test_cognito_auth():
    """Test Cognito authentication"""
    print("🔐 Testing Cognito Authentication for AgentCore")
    print("=" * 50)
    
    # Initialize Cognito client
    session = boto3.Session(profile_name=AWS_PROFILE)
    cognito_client = session.client('cognito-idp', region_name=REGION)
    
    try:
        # Authenticate user
        print(f"📧 Authenticating: {USERNAME}")
        
        response = cognito_client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': USERNAME,
                'PASSWORD': PASSWORD
            }
        )
        
        # Extract tokens
        auth_result = response['AuthenticationResult']
        access_token = auth_result['AccessToken']
        id_token = auth_result['IdToken']
        refresh_token = auth_result['RefreshToken']
        
        print("✅ Authentication successful!")
        print(f"🎫 Access Token: {access_token[:50]}...")
        print(f"🆔 ID Token: {id_token[:50]}...")
        print(f"🔄 Refresh Token: {refresh_token[:50]}...")
        
        # Get user info
        user_response = cognito_client.get_user(AccessToken=access_token)
        print(f"👤 User: {user_response['Username']}")
        print(f"📧 Email: {[attr['Value'] for attr in user_response['UserAttributes'] if attr['Name'] == 'email'][0]}")
        
        return {
            'access_token': access_token,
            'id_token': id_token,
            'refresh_token': refresh_token,
            'user_id': user_response['Username']
        }
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return None

def test_agentcore_with_cognito(tokens):
    """Test AgentCore with Cognito identity"""
    if not tokens:
        print("❌ No tokens available for AgentCore test")
        return
        
    print("\n🤖 Testing AgentCore with Cognito Identity")
    print("=" * 50)
    
    # Initialize AgentCore client
    session = boto3.Session(profile_name=AWS_PROFILE)
    agentcore_client = session.client('bedrock-agentcore', region_name=REGION)
    
    try:
        # Test with identity context
        response = agentcore_client.invoke_agent_runtime(
            agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgent-EqFCwr3WrQ',
            runtimeSessionId=f"cognito-{tokens['user_id'][:32]}",
            payload=json.dumps({
                'prompt': f'Hello! I am authenticated user {USERNAME}. Please remember my identity.',
                'user_context': {
                    'user_id': tokens['user_id'],
                    'email': USERNAME
                }
            })
        )
        
        result = json.loads(response['response'].read())
        
        if result['status'] == 'success':
            print("✅ AgentCore with Cognito identity successful!")
            print(f"📥 Response: {result['response']['content'][0]['text'][:100]}...")
            return True
        else:
            print(f"❌ AgentCore failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ AgentCore test failed: {e}")
        return False

if __name__ == "__main__":
    # Test authentication
    tokens = test_cognito_auth()
    
    # Test AgentCore integration
    test_agentcore_with_cognito(tokens)
    
    print(f"\n📋 Cognito Configuration:")
    print(f"   User Pool ID: {USER_POOL_ID}")
    print(f"   Client ID: {CLIENT_ID}")
    print(f"   Region: {REGION}")
    print(f"   Username: {USERNAME}")
