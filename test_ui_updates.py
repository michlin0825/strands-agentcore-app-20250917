#!/usr/bin/env python3
"""
Quick test to verify UI updates are working
"""

def test_ui_content():
    """Test that the UI files contain the updated content"""
    
    # Test minimal working app
    with open('streamlit_app/app_minimal_working.py', 'r') as f:
        content = f.read()
        
    print("🧪 Testing UI Updates")
    print("=" * 50)
    
    # Check title updates
    if "Strands AgentCore App" in content:
        print("✅ App title updated correctly")
    else:
        print("❌ App title not updated")
    
    # Check KB ID display
    if "VVJWR6EQPY" in content:
        print("✅ Knowledge Base ID displayed")
    else:
        print("❌ Knowledge Base ID missing")
    
    # Check MCP tools
    if "Tavily Web Search" in content:
        print("✅ Tavily tool listed")
    else:
        print("❌ Tavily tool missing")
        
    if "Bedrock Knowledge Base" in content:
        print("✅ Bedrock KB tool listed")
    else:
        print("❌ Bedrock KB tool missing")
    
    print("\n🎯 UI Features Added:")
    print("• Knowledge Base ID: VVJWR6EQPY")
    print("• MCP Tools: Tavily Web Search, Bedrock Knowledge Base")
    print("• Updated branding: Strands AgentCore App")
    print("\n🌐 Access at: http://localhost:8501")

if __name__ == "__main__":
    test_ui_content()
