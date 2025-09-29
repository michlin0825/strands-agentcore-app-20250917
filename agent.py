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

# Initialize Strands agent with enhanced autonomous reasoning
agent = Agent(
    tools=[web_search, knowledge_search],
    system_prompt="""You are an intelligent research assistant with autonomous reasoning capabilities.

For each query:
1. Analyze if you need current information (use web_search)
2. Check if domain knowledge is needed (use knowledge_search)  
3. For complex topics, use BOTH tools to cross-validate information
4. Think step-by-step and explain your reasoning
5. Provide comprehensive, well-researched responses

Always be thorough but concise. Use multiple tools when beneficial."""
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
