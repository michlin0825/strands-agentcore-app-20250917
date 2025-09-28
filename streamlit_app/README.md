# HelloWorld Strands Agent - Streamlit Frontend

## 🎯 Overview

Optimized web interface for the HelloWorld Strands Agent with proper Cognito authentication and AgentCore Runtime V2 integration.

## ✨ Features

- 🔐 **Cognito Authentication**: Secure login with email/password
- 💬 **Real-time Chat**: Fast, responsive conversation interface
- 🔍 **Web Search**: Tavily API integration for current information
- 📚 **RAG Knowledge Base**: Bedrock KB (VVJWR6EQPY) with Amazon shareholder letters
- 🧠 **Memory Integration**: Connected to explicit `helloworldmemory` resource
- 🔄 **Session Management**: Dynamic session IDs with proper memory isolation on reset
- ⚡ **Optimized Performance**: Fast startup with lazy loading
- 👤 **User Context**: Shows authenticated user in sidebar
- 🔄 **Session Management**: Reset chat and logout functionality

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- AWS credentials configured (CloudChef01 profile)
- Valid Cognito User Pool credentials

### Installation & Startup

```bash
# Navigate to streamlit app directory
cd streamlit_app

# Install minimal dependencies
pip install -r requirements.txt

# Start the application
./start.sh
```

## 📋 Current Configuration

### AgentCore Integration
- **Runtime ARN**: `HelloWorldStrandsAgentV2-R3GAODHoRb`
- **Memory Resource**: `helloworldmemory` (explicit AgentCore Memory)
- **Web Search**: Tavily API with constructor pattern integration
- **Knowledge Base**: Bedrock KB (`VVJWR6EQPY`) with Amazon shareholder letters
- **Region**: `us-east-1`
- **Profile**: `CloudChef01`

### Authentication
- **User Pool ID**: `us-east-1_LyhSJXjeF`
- **Client ID**: `2kiuoifa3ulekjbtdj4tngkt7h`
- **Auth Flow**: ADMIN_NO_SRP_AUTH

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Streamlit     │    │   AWS Cognito    │    │   AgentCore V2      │
│   Frontend      │◄──►│   User Pool      │    │   Runtime           │
│                 │    │                  │    │                     │
│ • Login Form    │    │ • Authentication │    │ • Strands Agent     │
│ • Chat UI       │    │ • User Identity  │    │ • Explicit Memory   │
│ • Session Mgmt  │    │ • Access Tokens  │    │ • Claude 3 Haiku    │
│                 │    │                  │    │ • Tavily Search     │
│                 │    │                  │    │ • Bedrock KB RAG    │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
```

## 📁 File Structure

```
streamlit_app/
├── app.py                 # Main optimized application
├── requirements.txt       # Minimal dependencies (streamlit, boto3)
├── start.sh              # Optimized startup script
├── .streamlit/
│   └── config.toml       # Clean Streamlit configuration
└── README.md             # This file
```

## 🔧 Key Components

### 1. Authentication Flow
- **Login Page**: Email/password form with Cognito integration
- **Validation**: Checks credentials against AWS Cognito User Pool
- **Session State**: Maintains authentication across app usage
- **Logout**: Clears session and returns to login

### 2. Chat Interface
- **Message Display**: Uses `st.chat_message()` for clean UI
- **Real-time Input**: `st.chat_input()` for responsive interaction
- **Message History**: Maintains conversation in session state
- **User Context**: Shows authenticated user email in sidebar

### 3. AgentCore Integration
- **Lazy Loading**: boto3 clients loaded only when needed
- **Cached Resources**: `@st.cache_resource` prevents reconnections
- **Error Handling**: Graceful error display for failed requests
- **Memory Integration**: Uses explicit `helloworldmemory` resource

## 🎨 User Interface

### Login Page
- Clean email/password form
- Authentication spinner during login
- Error messages for failed attempts
- Professional styling with centered layout

### Chat Interface
- **Header**: Shows app title
- **Sidebar**: User info, memory status, search capability, knowledge base info, controls
- **Messages**: Clean chat bubbles for user/assistant
- **Input**: Bottom chat input with placeholder text
- **Search Integration**: Automatic Tavily web search for current information
- **RAG Integration**: Automatic Bedrock Knowledge Base search for company information
- **Session Management**: Dynamic session IDs ensure proper memory isolation on reset

## 🔍 Authentication

### Login Process
1. Enter valid Cognito User Pool email/password
2. Click "Login" button
3. System authenticates with AWS Cognito
4. Successful login grants access to chat interface
5. Failed login shows specific error message

### Session Management
- Authentication state persists during app usage
- User email displayed in sidebar
- Logout button clears session and returns to login
- Reset chat button clears conversation history

## ⚡ Performance Optimizations

### Fast Startup
- **Lazy Imports**: Heavy modules loaded only when needed
- **Cached Clients**: AWS clients cached to prevent reconnections
- **Minimal Dependencies**: Only streamlit and boto3 required
- **Clean Config**: No deprecated Streamlit options

### Runtime Efficiency
- **Session Caching**: Prevents unnecessary re-authentication
- **Resource Caching**: AgentCore client cached across requests
- **Optimized UI**: Uses built-in Streamlit components

## 🔧 Configuration

### Streamlit Settings (`.streamlit/config.toml`)
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"

[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false
```

### Startup Script (`start.sh`)
```bash
#!/bin/bash
echo "🚀 Starting HelloWorld Strands Agent..."
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
streamlit run app.py --server.port 8501 2>/dev/null
```

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify Cognito User Pool credentials
   - Check AWS profile permissions
   - Ensure User Pool ID and Client ID are correct

2. **AgentCore Connection Issues**
   - Verify Runtime V2 is active
   - Check AWS credentials and region
   - Confirm `helloworldmemory` resource exists

3. **Startup Issues**
   - Ensure dependencies installed: `pip install -r requirements.txt`
   - Check AWS profile configured: `aws configure list --profile CloudChef01`
   - Verify port 8501 is available

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Session Management Issues
If "Reset Chat" doesn't clear memory:
1. **Check Session ID**: Verify new UUID is generated on reset
2. **Verify AgentCore Call**: Confirm dynamic session ID is used
3. **Clear Browser Cache**: Force refresh with Ctrl+F5
4. **Check Logs**: Look for session ID changes in CloudWatch

## 📊 Performance Metrics

- **Startup Time**: ~2-3 seconds (optimized)
- **Response Time**: 2-3 seconds average
- **Memory Usage**: Minimal with lazy loading
- **Authentication**: <1 second for valid credentials

## 🚀 Deployment Options

### Local Development
```bash
./start.sh
# Access at http://localhost:8501
```

### Production Deployment
- Deploy on AWS EC2/ECS with HTTPS
- Use environment variables for sensitive config
- Configure CloudWatch monitoring
- Set up load balancing for multiple instances

## 🔄 Session Management

### **Reset Chat Functionality**
- **Complete Reset**: Clears both Streamlit UI and AgentCore memory
- **Dynamic Session IDs**: Each reset generates new unique session ID
- **Memory Isolation**: Fresh conversations with no previous context
- **User Feedback**: Success message confirms reset completion

### **Session Behavior**
| Action | Streamlit State | AgentCore Memory | Result |
|--------|----------------|------------------|---------|
| **Normal Chat** | ✅ Preserved | ✅ Preserved | Conversation continues |
| **Reset Chat** | ❌ Cleared | ❌ New Session | Fresh start, no memory |
| **Logout** | ❌ Cleared | ❌ New Session | Complete reset |

### **Technical Implementation**
```python
# Generate unique session ID on reset
import uuid
st.session_state.session_id = str(uuid.uuid4())[:8]

# Use dynamic session ID in AgentCore calls
runtime_session_id = f"streamlit-session-{session_id}-..."
```

## 🎯 Usage Examples

### **Current Information (Web Search)**
- "What's the latest news about Taiwan?"
- "What's the weather in Tokyo today?"
- "Recent developments in AI technology"

### **Company Knowledge (RAG)**
- "What are the key highlights from Amazon shareholder letters?"
- "What does Jeff Bezos say about customer obsession?"
- "Tell me about Amazon's Day 1 mentality"

### **General Conversation**
- "Hello, how are you?"
- "Can you help me with a task?"
- "What can you do?"

**🤖 The agent automatically chooses the right tool based on your question!**

---

**Status**: ✅ **Optimized and Fully Operational with RAG + Search + Session Management**

**Key Features**: Fast startup, proper authentication, clean UI, AgentCore V2 integration, real-time web search, RAG knowledge base, proper session isolation

**Last Updated**: September 18, 2025 - Fixed session management and memory isolation on reset
