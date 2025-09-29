#!/usr/bin/env python3
"""
Strands AgentCore App with AgentCore native memory management
"""

import os
import json
import logging
from typing import Dict, Any
from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from web_search_tool import web_search
from knowledge_base_tool import knowledge_search

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment for tool consent
os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Initialize BedrockAgentCoreApp
app = BedrockAgentCoreApp()

# Initialize Strands agent with separated external and internal data sourcing tools
agent = Agent(
    tools=[web_search, knowledge_search],
    system_prompt="You are a helpful AI assistant with memory of our conversation. Provide concise, accurate, and direct answers. Use tools when needed for current information or specific knowledge. Reference previous conversation context when relevant."
)

@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Process user input with AgentCore native memory management"""
    try:
        user_message = payload.get("prompt", "Hello")
        session_id = payload.get("session_id", "default-session")
        
        logger.info(f"Processing message for session: {session_id[:20]}...")
        
        # Process with Strands agent - AgentCore handles memory via runtimeSessionId
        result = agent(user_message)
        
        return {
            "response": {
                "role": "assistant",
                "content": [{"text": result.message}]
            },
            "session_id": session_id,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return {
            "error": str(e),
            "session_id": payload.get("session_id", "unknown"),
            "status": "error"
        }

if __name__ == "__main__":
    logger.info("Starting Strands AgentCore App with native memory management...")
    app.run()
