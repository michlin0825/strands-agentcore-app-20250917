# Strands AgentCore App

A secure AI chat interface with real-time web search and knowledge base access, built with Amazon Bedrock AgentCore Runtime and Strands SDK.

## 🎯 Overview

**Secure AI Chat with Enhanced Capabilities:**
- 🔐 **Cognito Authentication** - Secure login with persistent sessions
- 🤖 **AI Conversations** - Powered by Bedrock AgentCore Runtime
- 🔍 **Real-time Web Search** - Current information via Tavily API
- 📚 **Knowledge Base Access** - Domain-specific queries using Bedrock Knowledge Base
- ⚡ **Modular Architecture** - Separated external and internal data sourcing

## 🏗️ Architecture

### Core Technologies
- **Amazon Bedrock AgentCore Runtime**: Serverless AI agent hosting with microVM isolation
- **Strands SDK**: Framework-agnostic agent development with modular MCP tool integration
- **Amazon Cognito**: User authentication with persistent session management
- **Streamlit**: Interactive web interface with real-time chat updates
- **Modular Tools**: Separated external (Tavily Web Search) and internal (Bedrock Knowledge Base) data sourcing

### Data Flow
```
User → Streamlit → Cognito Auth → AgentCore Runtime → Strands Agent → [Web Search | Knowledge Base] → Response
```

## 📸 Screenshots

| App Login | Q&A in Action |
|-----------|---------------|
| ![Login](screenshots/screenshot_1.png) | ![Chat](screenshots/screenshot_2.png) |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+, Docker Desktop, AWS CLI
- AWS Profile: `CloudChef01` with Bedrock AgentCore permissions
- Valid Cognito credentials

### Installation
```bash
# Navigate to project
cd /Users/mba/Desktop/strands-agentcore-app-20250917

# Activate environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your actual values

# Start the application
./start_env_app.sh
```

**Access**: http://localhost:8501

## 🔧 Configuration

### Environment Variables
```bash
# AWS & AgentCore
AWS_PROFILE=CloudChef01
AWS_REGION=us-east-1
AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/StrandsAgentCoreApp20250917-I3867LFr4j
KNOWLEDGE_BASE_ID=VVJWR6EQPY

# Cognito Authentication
COGNITO_USER_POOL_ID=us-east-1_LyhSJXjeF
COGNITO_CLIENT_ID=2kiuoifa3ulekjbtdj4tngkt7h
COGNITO_USERNAME=your_username_here
COGNITO_PASSWORD=your_password_here

# External APIs
TAVILY_API_KEY=your_tavily_api_key_here
```

## 🚀 Deployment

### Automated Deployment
```bash
python deploy_agentcore_v2.py
```

### Manual Runtime Creation
1. **AWS Console** → Bedrock → AgentCore → Create Runtime
2. **Name**: `StrandsAgentCoreApp20250917`
3. **Container URI**: `111735445051.dkr.ecr.us-east-1.amazonaws.com/strands-agentcore-app-20250917:latest`
4. **Environment Variables**: Set `TAVILY_API_KEY` and `KNOWLEDGE_BASE_ID`

**Detailed Steps**: See `MANUAL_RUNTIME_CREATION.md`

## 🔍 Implementation Details

### Modular Agent Architecture
```python
# agent.py - Main agent with separated data sourcing
from strands import Agent
from web_search_tool import web_search
from knowledge_base_tool import knowledge_search

agent = Agent(
    tools=[web_search, knowledge_search],
    system_prompt="Provide concise, accurate answers. Use tools for current information or specific knowledge."
)
```

### External Data Sourcing
```python
# web_search_tool.py - Tavily web search for current information
@tool
def web_search(query: str) -> str:
    """Search the web for current information using Tavily."""
    # Implementation details...
```

### Internal Data Sourcing
```python
# knowledge_base_tool.py - Bedrock Knowledge Base for domain knowledge
@tool
def knowledge_search(query: str) -> str:
    """Search company knowledge base for internal information."""
    # Implementation details...
```

### Authentication & Sessions
```python
# streamlit_app/app_env.py - Cognito authentication with persistent sessions
def authenticate_user(username, password):
    # Cognito authentication implementation
    
def set_persistent_session(email):
    # Session management with URL parameters
```

## 📁 Project Structure

```
strands-agentcore-app-20250917/
├── README.md                        # Project documentation
├── MANUAL_RUNTIME_CREATION.md       # Runtime creation guide
├── screenshots/                     # App screenshots
├── streamlit_app/
│   └── app_env.py                  # Main Streamlit app with Cognito auth
├── agent.py                        # Strands agent with modular data sourcing
├── web_search_tool.py              # External data sourcing (Tavily/MCP)
├── knowledge_base_tool.py          # Internal data sourcing (Bedrock KB/RAG)
├── Dockerfile                      # Container configuration
├── requirements.txt                # Python dependencies
├── deploy_agentcore_v2.py          # Deployment automation
├── start_env_app.sh               # Startup script
├── test_deployed_agent.py         # Agent connectivity testing
├── test_cognito_auth.py           # Authentication testing
├── test_response_parsing.py       # Response parsing validation
├── .env.example                   # Environment template
├── .env                           # Local environment variables
├── .gitignore                     # Git exclusions
└── venv/                          # Python virtual environment
```

## 🎯 Usage Examples

1. **Login**: Use Cognito credentials to authenticate
2. **Current Events**: "What's happening in AI today?" *(uses web_search_tool.py)*
3. **Technical Questions**: "Explain AWS Lambda concisely" *(uses knowledge_base_tool.py)*
4. **Knowledge Queries**: Domain-specific questions *(uses knowledge_base_tool.py)*
5. **Session Persistence**: Refresh page - stay logged in!

## 🧪 Testing & Troubleshooting

### Test Commands
```bash
python test_deployed_agent.py      # Test agent connectivity
python test_cognito_auth.py        # Test authentication
python test_response_parsing.py    # Test response parsing
```

### Common Issues
- **Authentication Failed**: Check Cognito credentials in `.env`
- **Runtime ARN Error**: Verify environment variable is set correctly
- **Session Not Persisting**: Check browser allows URL parameters
- **Module Import Error**: Ensure virtual environment is activated

## 📝 Version History

- **v4.0** (2025-09-28): Modular architecture with separated data sourcing tools, codebase cleanup
- **v3.0** (2025-01-28): Cognito authentication, persistent sessions, concise responses
- **v2.0** (2025-01-28): Environment-based configuration, updated naming
- **v1.0** (2025-01-28): Working implementation with response parsing

## 🔗 Resources

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Amazon Cognito Documentation](https://docs.aws.amazon.com/cognito/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Strands SDK Documentation](https://github.com/strands-ai/strands)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
