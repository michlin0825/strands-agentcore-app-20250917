#!/usr/bin/env python3
"""
Test script to verify response parsing logic
"""
import json

def extract_text_from_response(response_data):
    """Extract ONLY the text from the agent response"""
    if response_data.get('status') == 'success':
        response_content = response_data.get('response', {})
        
        # The format is: {'role': 'assistant', 'content': [{'text': 'ACTUAL_TEXT_HERE'}]}
        if (isinstance(response_content, dict) and 
            'content' in response_content and 
            isinstance(response_content['content'], list) and 
            len(response_content['content']) > 0 and
            'text' in response_content['content'][0]):
            
            # Extract ONLY the text string
            actual_text = response_content['content'][0]['text']
            return actual_text  # Return the raw text without any processing
        
        return "Error: Could not extract text from response"
    else:
        return f"Agent error: {response_data.get('error', 'Unknown error')}"

# Test with the exact format you're seeing
test_response = {
    "status": "success",
    "response": {
        "role": "assistant",
        "content": [
            {
                "text": "Based on the current weather information for Taipei:\n\n**Today's Weather in Taipei:**\n- **Temperature**: 27°C (about 81°F)\n- **Conditions**: Partly cloudy\n- **Wind**: Southeast at 3.6 mph\n- **Humidity**: 84%\n\nIt's a fairly warm and humid day in Taipei with partly cloudy skies. The high humidity is typical for the region, and the southeast winds are light. It's good weather for outdoor activities, though you might want to stay hydrated due to the humidity."
            }
        ]
    }
}

print("🧪 Testing Response Parsing")
print("=" * 50)

result = extract_text_from_response(test_response)
print("✅ Extracted text:")
print(result)
print("\n" + "=" * 50)
print("✅ Test completed - this should show ONLY the weather text without any dictionary formatting")
