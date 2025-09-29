import streamlit as st
import uuid
import boto3
import json
import os
from dotenv import load_dotenv
import hmac
import hashlib
import base64
import time

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AI Agent Powered by Bedrock AgentCore", page_icon="🤖")

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session-{str(uuid.uuid4())}"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

def check_persistent_session():
    """Check if user has a valid persistent session"""
    try:
        # Check for auth token in query params (simple persistent session)
        query_params = st.query_params
        if 'auth_token' in query_params:
            token = query_params['auth_token']
            # Simple token validation (in production, use proper JWT validation)
            if token and len(token) > 20:  # Basic validation
                stored_email = query_params.get('user', '')
                if stored_email:
                    st.session_state.authenticated = True
                    st.session_state.user_email = stored_email
                    return True
    except:
        pass
    return False

def set_persistent_session(email):
    """Set persistent session by updating URL params"""
    # Generate simple auth token (in production, use proper JWT)
    auth_token = base64.b64encode(f"{email}:{int(time.time())}".encode()).decode()
    
    # Update URL with auth parameters
    st.query_params.auth_token = auth_token
    st.query_params.user = email
    
def clear_persistent_session():
    """Clear persistent session"""
    st.query_params.clear()

def get_secret_hash(username, client_id, client_secret):
    """Generate secret hash for Cognito authentication"""
    message = username + client_id
    dig = hmac.new(client_secret.encode('UTF-8'), message.encode('UTF-8'), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def authenticate_user(username, password):
    """Authenticate user with Cognito"""
    try:
        client = boto3.client('cognito-idp', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        
        response = client.initiate_auth(
            ClientId=os.getenv('COGNITO_CLIENT_ID'),
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        
        if response.get('AuthenticationResult'):
            return True, response['AuthenticationResult']
        return False, None
        
    except Exception as e:
        return False, str(e)

def login_form():
    """Display login form"""
    st.title("🔐 Login Required")
    st.write("Please authenticate to access the AI Agent")
    
    with st.form("login_form"):
        username = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                with st.spinner("Authenticating..."):
                    success, result = authenticate_user(username, password)
                    
                if success:
                    # Generate fresh session ID for new login (ensures memory isolation)
                    st.session_state.session_id = f"session-{str(uuid.uuid4())}"
                    st.session_state.messages = []  # Fresh conversation history
                    st.session_state.authenticated = True
                    st.session_state.user_email = username
                    set_persistent_session(username)
                    st.success("✅ Authentication successful!")
                    st.rerun()
                else:
                    st.error(f"❌ Authentication failed: {result}")
            else:
                st.error("Please enter both email and password")

def get_aws_client():
    """Create AWS client using environment variables"""
    aws_profile = os.getenv('AWS_PROFILE')
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    
    if aws_profile:
        session = boto3.Session(profile_name=aws_profile)
        return session.client('bedrock-agentcore', region_name=aws_region)
    
    return boto3.client('bedrock-agentcore', region_name=aws_region)

def call_agent(prompt, session_id):
    """Call the deployed Strands agent"""
    try:
        agent_runtime_arn = os.getenv('AGENT_RUNTIME_ARN')
        if not agent_runtime_arn:
            return "Error: AGENT_RUNTIME_ARN environment variable not set"
        
        client = get_aws_client()
        
        payload = json.dumps({"prompt": prompt, "session_id": session_id})
        
        response = client.invoke_agent_runtime(
            agentRuntimeArn=agent_runtime_arn,
            runtimeSessionId=session_id,
            payload=payload
        )
        
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        
        if (response_data.get('status') == 'success' and
            'response' in response_data and
            'content' in response_data['response'] and
            len(response_data['response']['content']) > 0 and
            'text' in response_data['response']['content'][0] and
            isinstance(response_data['response']['content'][0]['text'], dict) and
            'content' in response_data['response']['content'][0]['text'] and
            len(response_data['response']['content'][0]['text']['content']) > 0 and
            'text' in response_data['response']['content'][0]['text']['content'][0]):
            
            return response_data['response']['content'][0]['text']['content'][0]['text']
        
        return "Failed to extract text from deeply nested response"
            
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Check for persistent session first
    if not st.session_state.authenticated:
        if check_persistent_session():
            st.rerun()
    
    # Check authentication
    if not st.session_state.authenticated:
        login_form()
        return
    
    # Main app interface for authenticated users
    st.title("🤖 AI Agent Powered by Bedrock AgentCore")
    
    # Get Knowledge Base ID from environment
    kb_id = os.getenv('KNOWLEDGE_BASE_ID', 'Not configured')
    
    with st.sidebar:
        st.write(f"**User:** {st.session_state.user_email}")
        st.write("**Session:** " + st.session_state.session_id[:20] + "...")
        st.write("**Status:** Connected to Agent")
        
        st.divider()
        st.write("**Configuration:**")
        st.write(f"• AWS Region: {os.getenv('AWS_REGION', 'us-east-1')}")
        st.write(f"• AWS Profile: {os.getenv('AWS_PROFILE', 'Default')}")
        
        st.divider()
        st.write("**MCP Tools:**")
        st.write("• 🔍 Tavily Web Search")
        st.write(f"• 📚 Bedrock Knowledge Base ({kb_id})")
        
        st.divider()
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = []
            st.session_state.session_id = f"session-{str(uuid.uuid4())}"  # Fresh session for memory isolation
            st.rerun()
            
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.messages = []
            st.session_state.session_id = f"session-{str(uuid.uuid4())}"  # Fresh session for next login
            clear_persistent_session()
            st.rerun()
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get agent response
        with st.spinner("Thinking..."):
            response = call_agent(prompt, st.session_state.session_id)
        
        # Add assistant response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to display the new messages
        st.rerun()

if __name__ == "__main__":
    main()
