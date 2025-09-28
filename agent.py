#!/usr/bin/env python3
"""
Strands AgentCore App with Tavily Search + Bedrock Knowledge Base
"""

import os
import json
import logging
from typing import Dict, Any
from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from tavily_tool import web_search, knowledge_search

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment for tool consent
os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Initialize BedrockAgentCoreApp
app = BedrockAgentCoreApp()

# Initialize Strands agent with both web search and knowledge base tools
agent = Agent(
    tools=[web_search, knowledge_search],
    system_prompt="You are a helpful AI assistant. Provide concise, accurate, and direct answers. Use tools when needed for current information or specific knowledge. Keep responses brief while maintaining factual accuracy."
)

@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Process user input and return a response"""
    try:
        user_message = payload.get("prompt", "Hello")
        session_id = payload.get("session_id", "default-session")
        memory_id = payload.get("memory_id", "helloworldmemory")
        
        logger.info(f"Processing: {user_message}")
        
        # Process with Strands agent (now with both Tavily search and Knowledge Base)
        result = agent(user_message)
        
        return {
            "response": {
                "role": "assistant",
                "content": [{"text": result.message}]
            },
            "session_id": session_id,
            "memory_id": memory_id,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "error": str(e),
            "session_id": payload.get("session_id", "unknown"),
            "status": "error"
        }

if __name__ == "__main__":
    logger.info("Starting Strands AgentCore App with Tavily + Knowledge Base...")
    app.run()
