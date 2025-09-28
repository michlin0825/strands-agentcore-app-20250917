#!/usr/bin/env python3
"""
Ultra-minimal test agent
"""

import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Ultra-minimal handler"""
    try:
        user_message = payload.get("prompt", "Hello")
        session_id = payload.get("session_id", "test-session")
        memory_id = payload.get("memory_id", "helloworldmemory")
        
        logger.info(f"Received: {user_message}")
        
        # Simple hardcoded response
        response_text = f"Hello! I received your message: '{user_message}'. This is a test response from the ultra-minimal agent."
        
        return {
            "response": {
                "role": "assistant",
                "content": [{"text": response_text}]
            },
            "session_id": session_id,
            "memory_id": memory_id,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "error": str(e),
            "status": "error"
        }

# For AgentCore compatibility
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Handle direct invocation with payload
        payload_str = sys.argv[1]
        payload = json.loads(payload_str)
        result = invoke(payload)
        print(json.dumps(result))
    else:
        # Simple HTTP server for testing
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8'))
                
                result = invoke(payload)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
        
        logger.info("Starting ultra-minimal agent on port 8080...")
        server = HTTPServer(('0.0.0.0', 8080), Handler)
        server.serve_forever()
