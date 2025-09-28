"""
Tavily search tool and Bedrock Knowledge Base for Strands agents
"""

import os
import requests
import logging
import boto3
from strands import tool

logger = logging.getLogger(__name__)

@tool
def web_search(query: str) -> str:
    """
    Search the web for current information using Tavily.
    Use this when you need up-to-date information, news, or facts.
    
    Args:
        query: The search query string
        
    Returns:
        Search results with relevant information
    """
    api_key = os.getenv('TAVILY_API_KEY', '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')
    
    if not api_key:
        return "Web search is not available (no API key configured)."
    
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": True,
            "include_images": False,
            "include_raw_content": False,
            "max_results": 3
        }
        
        logger.info(f"Searching Tavily for: {query}")
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Format results
        results = []
        
        # Add direct answer if available
        if data.get('answer'):
            results.append(f"**Answer:** {data['answer']}")
        
        # Add search results
        if data.get('results'):
            results.append("**Sources:**")
            for i, result in enumerate(data['results'][:3], 1):
                title = result.get('title', 'No title')
                content = result.get('content', 'No content')
                url = result.get('url', 'No URL')
                
                # Truncate content if too long
                if len(content) > 150:
                    content = content[:150] + "..."
                
                results.append(f"{i}. {title}")
                results.append(f"   {content}")
                results.append(f"   {url}")
        
        return "\n".join(results) if results else "No search results found."
        
    except Exception as e:
        logger.error(f"Tavily search error: {e}")
        return f"Search failed: {str(e)}"

@tool
def knowledge_search(query: str) -> str:
    """
    Search company knowledge base for internal information.
    Use this for company policies, procedures, documentation, and internal knowledge.
    
    Args:
        query: The search query string
        
    Returns:
        Relevant information from company knowledge base
    """
    knowledge_base_id = os.getenv('BEDROCK_KB_ID', 'VVJWR6EQPY')
    
    try:
        session = boto3.Session(profile_name="CloudChef01")
        client = session.client('bedrock-agent-runtime', region_name='us-east-1')
        
        logger.info(f"Searching Knowledge Base {knowledge_base_id} for: {query}")
        
        response = client.retrieve_and_generate(
            input={'text': query},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0'
                }
            }
        )
        
        return response['output']['text']
        
    except Exception as e:
        logger.error(f"Knowledge base search error: {e}")
        return f"Knowledge search failed: {str(e)}"
