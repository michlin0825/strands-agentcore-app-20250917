import streamlit as st
import json
import uuid
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

st.set_page_config(page_title="HelloWorld Strands Agent", page_icon="🤖")

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

@st.cache_resource
def get_agentcore_client():
    """Initialize AgentCore client with proper error handling"""
    try:
        session = boto3.Session(profile_name="CloudChef01")
        client = session.client('bedrock-agentcore', region_name='us-east-1')
        
        # Test connection
        client.list_agent_runtimes()
        
        def invoke(msg):
            try:
                session_id = st.session_state.get('session_id', 'default')
                runtime_session_id = f"streamlit-{session_id}"
                
                resp = client.invoke_agent_runtime(
                    agentRuntimeArn="arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgentV2-R3GAODHoRb",
                    runtimeSessionId=runtime_session_id,
                    payload=json.dumps({
                        'prompt': msg, 
                        'session_id': runtime_session_id, 
                        'memory_id': 'helloworldmemory'
                    })
                )
                result = json.loads(resp['response'].read())
                if result['status'] == 'success':
                    return result['response']['content'][0]['text']
                else:
                    return f"Agent Error: {result.get('error', 'Unknown error')}"
            except Exception as e:
                return f"Invocation Error: {str(e)}"
        
        return invoke
        
    except NoCredentialsError:
        st.error("❌ AWS credentials not found. Please configure CloudChef01 profile.")
        return None
    except ClientError as e:
        st.error(f"❌ AWS Client Error: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return None

def main():
    st.title("🤖 HelloWorld Strands Agent")
    
    # Check if client is available
    client = get_agentcore_client()
    
    with st.sidebar:
        st.write("**Session:** " + st.session_state.session_id)
        st.write("**Memory:** helloworldmemory")
        st.write("**Search:** Tavily API enabled")
        
        if client:
            st.success("✅ AgentCore Connected")
        else:
            st.error("❌ AgentCore Disconnected")
            st.info("💡 The app will work in demo mode")
        
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())[:8]
            st.success("✅ Chat reset!")
            st.rerun()
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if client:
                    try:
                        response = client(prompt)
                        st.write(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                else:
                    # Demo mode response
                    demo_response = f"🤖 Demo Mode: I received your message '{prompt}'. The AgentCore connection is not available, but the Streamlit app is working correctly!"
                    st.write(demo_response)
                    st.session_state.messages.append({"role": "assistant", "content": demo_response})

if __name__ == "__main__":
    main()
