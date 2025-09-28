#!/usr/bin/env python3
"""
Minimal HelloWorld Strands Agent for testing
"""

import os
import json
import logging
from typing import Dict, Any
from strands_agents import Agent, app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple agent without tools
agent = Agent(
    name="HelloWorldMinimal",
    model="anthropic.claude-3-haiku-20240307-v1:0",
    instructions="You are a helpful AI assistant. Respond clearly and concisely."
)

@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Minimal agent invocation handler"""
    try:
        user_message = payload.get("prompt", "")
        session_id = payload.get("session_id", "default-session")
        memory_id = payload.get("memory_id", "helloworldmemory")
        
        if not user_message:
            return {
                "error": "No prompt provided",
                "session_id": session_id
            }
        
        logger.info(f"Processing: {user_message[:50]}...")
        
        # Simple response without tools
        response = agent.run(user_message)
        assistant_message = response.content[0].text
        
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
        logger.error(f"Error: {e}")
        return {
            "error": str(e),
            "session_id": payload.get("session_id", "unknown"),
            "status": "error"
        }

if __name__ == "__main__":
    logger.info("Starting minimal HelloWorld Strands Agent...")
    app.run(host="0.0.0.0", port=8080)
