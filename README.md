# AI Agent Powered by Bedrock AgentCore

A secure, intelligent chat interface that combines AI conversations with real-time web search and knowledge base access, built with Streamlit and Amazon Bedrock AgentCore Runtime.

## 📋 What This App Does

**Secure AI Chat with Enhanced Capabilities:**
- 🔐 **Cognito Authentication** - Secure login with persistent sessions
- 🤖 **AI Conversations** - Powered by Bedrock AgentCore Runtime with Strands SDK
- 🔍 **Real-time Web Search** - Current information via Tavily API
- 📚 **Knowledge Base Access** - Domain-specific queries using Bedrock Knowledge Base
- ⚡ **Concise Responses** - Optimized for direct, factual answers

**Perfect for**: Research assistance, current events, technical questions, and scenarios requiring both real-time web data and curated knowledge.

## 🏗️ Architecture & Technology Stack

```mermaid
sequenceDiagram
    participant User
    participant Streamlit as Streamlit App
    participant Cognito as Amazon Cognito
    participant AgentCore as Bedrock AgentCore Runtime
    participant Strands as Strands Agent
    participant Tavily as Tavily Web Search
    participant KB as Bedrock Knowledge Base

    User->>Streamlit: Access webapp
    Streamlit->>Cognito: Authenticate user
    Cognito-->>Streamlit: Return auth token
    Streamlit-->>User: Show chat interface

    User->>Streamlit: Send message
    Streamlit->>AgentCore: Invoke agent runtime
    AgentCore->>Strands: Process with MCP tools
    
    alt Web search needed
        Strands->>Tavily: Search web for current info
        Tavily-->>Strands: Return search results
    end
    
    alt Knowledge base query
        Strands->>KB: Query domain knowledge
        KB-->>Strands: Return relevant documents
    end
    
    Strands-->>AgentCore: Generate response
    AgentCore-->>Streamlit: Return nested response
    Streamlit->>Streamlit: Parse response structure
    Streamlit-->>User: Display clean answer
```

### Core Technologies
- **Amazon Bedrock AgentCore Runtime**: Serverless AI agent hosting with microVM isolation and 8-hour execution time
- **Strands SDK**: Framework-agnostic agent development with MCP tool integration
- **Amazon Cognito**: User authentication with persistent session management
- **Streamlit**: Interactive web interface with real-time chat updates
- **MCP Tools**: Tavily Web Search + Bedrock Knowledge Base (ID: VVJWR6EQPY)

## 📸 Screenshots

### App Login
![App Login](screenshots/screenshot_1.png)

### Q&A in Action
![Q&A in Action](screenshots/screenshot_2.png)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+, Docker Desktop, AWS CLI
- AWS Profile: `CloudChef01` with Bedrock AgentCore permissions
- Valid Cognito credentials

### Installation & Setup
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

### Runtime Configuration
- **Runtime ARN**: `arn:aws:bedrock-agentcore:us-east-1:111735445051:runtime/StrandsAgentCoreApp20250917-I3867LFr4j`
- **Container**: `111735445051.dkr.ecr.us-east-1.amazonaws.com/strands-agentcore-app-20250917:latest`
- **Knowledge Base**: `VVJWR6EQPY`

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
```

## 🚀 Deployment

### Automated Process
```bash
python deploy_agentcore_v2.py
```

**Steps**: ECR repository creation → Docker build/push → Manual runtime creation via AWS Console

### Manual Runtime Creation
1. **AWS Console** → Bedrock → AgentCore → Create Runtime
2. **Name**: `StrandsAgentCoreApp20250917`
3. **Container URI**: `111735445051.dkr.ecr.us-east-1.amazonaws.com/strands-agentcore-app-20250917:latest`
4. **Environment Variables**: `TAVILY_API_KEY`, `BEDROCK_KNOWLEDGE_BASE_ID`

## 🔍 Key Implementation Details

### Strands Agent with MCP Tools
```python
# agent.py - Strands agent with optimized prompt
from strands import Agent
from tavily_tool import web_search, knowledge_search

agent = Agent(
    tools=[web_search, knowledge_search],
    system_prompt="You are a helpful AI assistant. Provide concise, accurate, and direct answers. Use tools when needed for current information or specific knowledge. Keep responses brief while maintaining factual accuracy."
)
```

### Cognito Authentication & Persistent Sessions
```python
def authenticate_user(username, password):
    client = boto3.client('cognito-idp', region_name=os.getenv('AWS_REGION'))
    response = client.initiate_auth(
        ClientId=os.getenv('COGNITO_CLIENT_ID'),
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={'USERNAME': username, 'PASSWORD': password}
    )
    return response.get('AuthenticationResult') is not None

def set_persistent_session(email):
    auth_token = base64.b64encode(f"{email}:{int(time.time())}".encode()).decode()
    st.query_params.auth_token = auth_token
    st.query_params.user = email
```

### AgentCore Response Parsing
```python
# Extract from deeply nested structure
return response_data['response']['content'][0]['text']['content'][0]['text']
```

## 🧪 Testing & Troubleshooting

### Test Commands
```bash
python test_deployed_agent.py      # Test agent connectivity
python test_cognito_auth.py        # Test authentication
```

### Common Issues
- **Authentication Failed**: Check Cognito credentials in `.env`
- **Runtime ARN Error**: Verify environment variable is set correctly
- **Session Not Persisting**: Check browser allows URL parameters

## 📁 Project Structure

```
strands-agentcore-app-20250917/
├── README.md
├── screenshots/                      # App screenshots
├── streamlit_app/app_env.py         # Main app with Cognito auth
├── agent.py                         # Strands agent with concise prompt
├── tavily_tool.py                   # MCP tools (web search + KB)
├── deploy_agentcore_v2.py           # Deployment automation
├── test_deployed_agent.py           # Testing scripts
├── .env / .env.example              # Environment configuration
└── start_env_app.sh                 # Startup script
```

## 🎯 Usage Examples

1. **Login**: Use Cognito credentials to authenticate
2. **Current Events**: "What's happening in AI today?"
3. **Technical Questions**: "Explain AWS Lambda concisely"
4. **Knowledge Queries**: Domain-specific questions using configured KB
5. **Session Persistence**: Refresh page - stay logged in!

## 📝 Version History

- **v3.0** (2025-01-28): Cognito authentication, persistent sessions, concise responses
- **v2.0** (2025-01-28): Environment-based configuration, updated naming
- **v1.0** (2025-01-28): Working implementation with response parsing

## 🔗 Resources

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Amazon Cognito Documentation](https://docs.aws.amazon.com/cognito/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)

---

**License**: MIT License - see [LICENSE](LICENSE) file for details.
