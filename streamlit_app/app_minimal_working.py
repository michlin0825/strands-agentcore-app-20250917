import streamlit as st
import uuid
import boto3
import json
import os

st.set_page_config(page_title="Strands AgentCore App", page_icon="🤖")

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"streamlit-session-{str(uuid.uuid4())}"

def polish_response(response):
    """Clean and format the agent response - only works on strings"""
    if not isinstance(response, str):
        return response  # Return as-is if not a string
    
    if not response:
        return "I apologize, but I couldn't generate a response."
    
    # Remove excessive whitespace
    response = ' '.join(response.split())
    
    # Ensure proper sentence ending
    if response and not response.endswith(('.', '!', '?')):
        response += '.'
    
    return response

def call_agent(prompt, session_id):
    """Call the deployed Strands agent"""
    try:
        session = boto3.Session(profile_name="CloudChef01")
        client = session.client('bedrock-agentcore', region_name='us-east-1')
        
        # Prepare payload
        payload = json.dumps({
            "prompt": prompt,
            "session_id": session_id
        })
        
        # Invoke agent
        response = client.invoke_agent_runtime(
            agentRuntimeArn="arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/HelloWorldStrandsAgentV2-R3GAODHoRb",
            runtimeSessionId=session_id,
            payload=payload
        )
        
        # Parse streaming response
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        
        # Extract ONLY the text - be very explicit
        if response_data.get('status') == 'success':
            response_content = response_data.get('response', {})
            
            # The format is: {'role': 'assistant', 'content': [{'text': 'ACTUAL_TEXT_HERE'}]}
            if (isinstance(response_content, dict) and 
                'content' in response_content and 
                isinstance(response_content['content'], list) and 
                len(response_content['content']) > 0 and
                'text' in response_content['content'][0]):
                
                # Extract ONLY the text string
                actual_text = response_content['content'][0]['text']
                return actual_text  # Return the raw text without any processing
            
            return "Error: Could not extract text from response"
        else:
            return f"Agent error: {response_data.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Connection error: {str(e)}"

def main():
    st.title("🤖 Strands AgentCore App")
    
    with st.sidebar:
        st.write("**Session:** " + st.session_state.session_id)
        st.write("**Status:** Connected to Agent")
        
        st.divider()
        st.write("**MCP Tools:**")
        st.write("• 🔍 Tavily Web Search")
        st.write("• 📚 Bedrock Knowledge Base (VVJWR6EQPY)")
        
        st.divider()
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = []
            st.session_state.session_id = f"streamlit-session-{str(uuid.uuid4())}"
            st.success("✅ Chat reset!")
            st.rerun()
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = call_agent(prompt, st.session_state.session_id)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
