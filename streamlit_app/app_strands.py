import streamlit as st
import uuid
from strands import Agent

st.set_page_config(page_title="HelloWorld Strands Agent", page_icon="🤖")

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

@st.cache_resource
def get_strands_agent():
    """Initialize Strands Agent"""
    try:
        # Create agent with default settings (uses AWS Bedrock)
        agent = Agent()
        return agent
    except Exception as e:
        st.error(f"Failed to initialize Strands Agent: {e}")
        return None

def main():
    st.title("🤖 HelloWorld Strands Agent")
    
    # Get agent
    agent = get_strands_agent()
    
    with st.sidebar:
        st.write("**Session:** " + st.session_state.session_id)
        st.write("**Framework:** Strands SDK")
        st.write("**Model:** Amazon Bedrock")
        
        if agent:
            st.success("✅ Strands Agent Ready")
        else:
            st.error("❌ Agent Initialization Failed")
        
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
                if agent:
                    try:
                        response = agent(prompt)
                        st.write(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"Agent Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                else:
                    # Fallback response
                    fallback_response = f"❌ Agent not available. Your message: '{prompt}'"
                    st.write(fallback_response)
                    st.session_state.messages.append({"role": "assistant", "content": fallback_response})

if __name__ == "__main__":
    main()
