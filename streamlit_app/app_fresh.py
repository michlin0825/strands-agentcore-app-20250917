import streamlit as st
import uuid
import boto3
import json

st.set_page_config(page_title="Strands AgentCore App", page_icon="🤖")

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"streamlit-session-{str(uuid.uuid4())}"

def call_agent(prompt, session_id):
    """Call the deployed Strands agent"""
    try:
        session = boto3.Session(profile_name="CloudChef01")
        client = session.client('bedrock-agentcore', region_name='us-east-1')
        
        payload = json.dumps({"prompt": prompt, "session_id": session_id})
        
        response = client.invoke_agent_runtime(
            agentRuntimeArn="arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgentV2-R3GAODHoRb",
            runtimeSessionId=session_id,
            payload=payload
        )
        
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        
        # The actual structure is deeply nested:
        # response_data['response']['content'][0]['text']['content'][0]['text']
        
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
    st.title("🤖 Strands AgentCore App")
    
    with st.sidebar:
        st.write("**Session:** " + st.session_state.session_id[:20] + "...")
        st.write("**Status:** Connected to Agent")
        
        st.divider()
        st.write("**MCP Tools:**")
        st.write("• 🔍 Tavily Web Search")
        st.write("• 📚 Bedrock Knowledge Base (VVJWR6EQPY)")
        
        st.divider()
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = []
            st.session_state.session_id = f"streamlit-session-{str(uuid.uuid4())}"
            st.rerun()
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = call_agent(prompt, st.session_state.session_id)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
