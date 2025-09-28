"""
Strands Agent with Bedrock Claude Sonnet and AgentCore Memory
Multi-turn conversation support with short-term memory and web search
"""

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models.bedrock import BedrockModel
import boto3
import json
import logging
import os
import requests
from typing import Dict, Any, Optional

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Get configuration from environment
AWS_PROFILE = os.getenv('AWS_PROFILE', 'CloudChef01')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
BEDROCK_MODEL = os.getenv('BEDROCK_MODEL', 'anthropic.claude-3-haiku-20240307-v1:0')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
MEMORY_NAME = "helloworldmemory"  # Explicit AgentCore Memory resource

# Initialize Bedrock model for Claude Sonnet
bedrock_model = BedrockModel(
    model_id=BEDROCK_MODEL
)

# Initialize Strands agent
agent = Agent(
    name="HelloWorld Assistant",
    description="A helpful assistant powered by Claude Sonnet with memory capabilities",
    model=bedrock_model,
    system_prompt="""You are a helpful AI assistant powered by Claude Sonnet. 
    You have access to conversation history and can maintain context across multiple turns.
    Be conversational, helpful, and remember what the user has told you in this session."""
)

# Memory client for AgentCore
memory_client = None

def get_memory_client():
    """Initialize memory client if not already done"""
    global memory_client
    if memory_client is None:
        try:
            # Use CloudChef01 profile credentials
            session = boto3.Session(profile_name=AWS_PROFILE)
            memory_client = session.client('bedrock-agentcore-memory', region_name=AWS_REGION)
            logger.info(f"Memory client initialized successfully with {AWS_PROFILE} profile")
        except Exception as e:
            logger.warning(f"Could not initialize memory client: {e}")
            memory_client = False
    return memory_client if memory_client is not False else None

def retrieve_conversation_history(session_id: str, memory_id: str) -> str:
    """Retrieve conversation history from AgentCore Memory"""
    client = get_memory_client()
    if not client:
        return ""
    
    try:
        response = client.get_memories(
            memoryId=memory_id,
            sessionId=session_id,
            maxResults=10
        )
        
        memories = response.get('memories', [])
        if memories:
            history = "\n".join([
                memory.get('content', {}).get('text', '') 
                for memory in memories
            ])
            logger.info(f"Retrieved {len(memories)} memories for session {session_id}")
            return f"Previous conversation:\n{history}\n\n"
        
    except Exception as e:
        logger.warning(f"Could not retrieve memories: {e}")
    
    return ""

def store_conversation_turn(session_id: str, memory_id: str, user_message: str, assistant_response: str):
    """Store conversation turn in AgentCore Memory"""
    client = get_memory_client()
    if not client:
        return
    
    try:
        conversation_turn = f"User: {user_message}\nAssistant: {assistant_response}"
        
        client.create_memory(
            memoryId=memory_id,
            sessionId=session_id,
            content={
                "text": conversation_turn
            }
        )
        logger.info(f"Stored conversation turn for session {session_id}")
        
    except Exception as e:
        logger.warning(f"Could not store memory: {e}")

def tavily_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using Tavily API
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        
    Returns:
        Formatted search results as string
    """
    if not TAVILY_API_KEY:
        return "Web search is not available - API key not configured."
    
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "max_results": max_results,
            "search_depth": "basic",
            "include_answer": True,
            "include_raw_content": False
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Format results
        results = []
        
        # Add direct answer if available
        if data.get('answer'):
            results.append(f"**Direct Answer:** {data['answer']}")
        
        # Add search results
        if data.get('results'):
            results.append("**Search Results:**")
            for i, result in enumerate(data['results'][:max_results], 1):
                title = result.get('title', 'No title')
                content = result.get('content', 'No content')
                url = result.get('url', 'No URL')
                
                # Truncate content if too long
                if len(content) > 200:
                    content = content[:200] + "..."
                
                results.append(f"{i}. **{title}**")
                results.append(f"   {content}")
                results.append(f"   Source: {url}")
        
        return "\n".join(results) if results else "No search results found."
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Tavily search request failed: {e}")
        return f"Search failed due to network error: {str(e)}"
    except Exception as e:
        logger.error(f"Tavily search error: {e}")
        return f"Search failed: {str(e)}"

# Register Tavily search as a tool for the agent
@agent.tool
def web_search(query: str) -> str:
    """
    Search the web for current information using Tavily.
    Use this when you need up-to-date information, news, or facts that might not be in your training data.
    
    Args:
        query: The search query string
        
    Returns:
        Search results with relevant information
    """
    logger.info(f"Performing web search for: {query}")
    return tavily_search(query)

@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Main agent invocation handler"""
    try:
        # Extract input parameters
        user_message = payload.get("prompt", "")
        session_id = payload.get("session_id", "default-session")
        memory_id = payload.get("memory_id", "helloworld-memory")
        
        if not user_message:
            return {
                "error": "No prompt provided. Please include a 'prompt' field in your request.",
                "session_id": session_id
            }
        
        logger.info(f"Processing request for session: {session_id}")
        
        # Retrieve conversation history
        conversation_history = retrieve_conversation_history(session_id, memory_id)
        
        # Prepare the full prompt with history
        full_prompt = f"{conversation_history}Current user message: {user_message}"
        
        # Get response from Strands agent
        response = agent.run(full_prompt)
        assistant_message = response.content[0].text
        
        # Store this conversation turn
        store_conversation_turn(session_id, memory_id, user_message, assistant_message)
        
        return {
            "response": {
                "role": "assistant", 
                "content": [{"text": assistant_message}]
            },
            "session_id": session_id,
            "memory_id": memory_id,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return {
            "error": f"Failed to process request: {str(e)}",
            "session_id": payload.get("session_id", "unknown"),
            "status": "error"
        }

def health():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "HelloWorld Strands Agent"}

if __name__ == "__main__":
    logger.info("Starting HelloWorld Strands Agent with AgentCore Runtime...")
    app.run(host="0.0.0.0", port=8080)
