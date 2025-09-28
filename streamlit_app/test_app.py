import streamlit as st
import uuid

st.set_page_config(page_title="HelloWorld Agent Test", page_icon="🤖")

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

def mock_agent_response(prompt):
    """Mock agent response for testing"""
    return f"Mock response to: {prompt}"

def main():
    st.title("🤖 HelloWorld Agent (Test Mode)")
    
    with st.sidebar:
        st.write("**Status:** Test Mode")
        st.write("**Session:** " + st.session_state.session_id)
        
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
        
        # Mock response
        with st.chat_message("assistant"):
            response = mock_agent_response(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
