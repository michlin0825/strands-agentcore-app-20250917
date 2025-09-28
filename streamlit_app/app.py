import streamlit as st

st.set_page_config(page_title="HelloWorld Agent", page_icon="🤖")

# Initialize session
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'session_id' not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())[:8]

@st.cache_resource
def get_cognito_client():
    import boto3
    session = boto3.Session(profile_name="CloudChef01")
    return session.client('cognito-idp', region_name='us-east-1')

@st.cache_resource
def get_agentcore_client():
    import boto3, json
    session = boto3.Session(profile_name="CloudChef01")
    client = session.client('bedrock-agentcore', region_name='us-east-1')
    
    def invoke(msg):
        try:
            # Use dynamic session ID from Streamlit state
            session_id = st.session_state.get('session_id', 'default')
            runtime_session_id = f"streamlit-session-{session_id}-12345678901234567890123456789012345678901234567890"
            
            resp = client.invoke_agent_runtime(
                agentRuntimeArn="arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgentV2-R3GAODHoRb",
                runtimeSessionId=runtime_session_id,
                payload=json.dumps({
                    'prompt': msg, 
                    'session_id': f'streamlit-{session_id}', 
                    'memory_id': 'helloworldmemory'
                })
            )
            result = json.loads(resp['response'].read())
            if result['status'] == 'success':
                # Extract just the text content, not the full structure
                return result['response']['content'][0]['text']
            else:
                return f"Error: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    return invoke

def authenticate_user(email, password):
    """Authenticate user with Cognito"""
    try:
        client = get_cognito_client()
        response = client.admin_initiate_auth(
            UserPoolId="us-east-1_LyhSJXjeF",
            ClientId="2kiuoifa3ulekjbtdj4tngkt7h",
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        
        return {
            'success': True,
            'email': email,
            'access_token': response['AuthenticationResult']['AccessToken']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def login_page():
    """Login page with email/password form"""
    st.title("🤖 Strands AgentCore App")
    st.markdown("### 🔐 Please Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            if st.form_submit_button("Login", type="primary", use_container_width=True):
                if email and password:
                    with st.spinner("Authenticating..."):
                        result = authenticate_user(email, password)
                    
                    if result['success']:
                        st.session_state.authenticated = True
                        st.session_state.user_info = result
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error(f"❌ Login failed: {result['error']}")
                else:
                    st.warning("⚠️ Please enter both email and password")

def chat_page():
    """Chat interface for authenticated users"""
    st.title("🤖 Strands AgentCore App")
    
    with st.sidebar:
        st.write(f"**User:** {st.session_state.user_info['email']}")
        st.write("**Memory:** helloworldmemory")
        
        st.divider()
        st.write("**MCP Tools:**")
        st.write("• 🔍 Tavily Web Search")
        st.write("• 📚 Bedrock Knowledge Base")
        
        st.divider()
        if st.button("🔄 Reset Chat"):
            # Clear Streamlit session state
            st.session_state.messages = []
            
            # Generate new session ID to isolate memory
            import uuid
            st.session_state.session_id = str(uuid.uuid4())[:8]
            
            st.success("✅ Chat reset! Starting fresh conversation.")
            st.rerun()
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.session_state.messages = []
            st.rerun()
    
    # Display all messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                client = get_agentcore_client()
                raw_response = client(prompt)
                
                # Debug: Check what we're getting
                if isinstance(raw_response, dict):
                    # If it's a dict, extract the text
                    if 'content' in raw_response and isinstance(raw_response['content'], list):
                        response = raw_response['content'][0]['text']
                    elif 'text' in raw_response:
                        response = raw_response['text']
                    else:
                        response = str(raw_response)
                else:
                    # If it's already a string, use it directly
                    response = raw_response
                    
            st.write(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    """Main application"""
    if not st.session_state.authenticated:
        login_page()
    else:
        chat_page()

if __name__ == "__main__":
    main()
