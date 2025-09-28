"""
Bedrock Knowledge Base tool for internal data sourcing (RAG)
"""

import os
import logging
import boto3
from strands import tool

logger = logging.getLogger(__name__)

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
