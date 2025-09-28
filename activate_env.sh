#!/bin/bash

# Strands AgentCore Environment Activation Script
echo "🚀 Activating Strands AgentCore Environment..."

# Navigate to project directory
cd /Users/mba/Desktop/strands-agentcore-app-20250917

# Activate virtual environment
source venv/bin/activate

# Verify key dependencies
echo "📦 Checking dependencies..."
if pip list | grep -q "strands-agents"; then
    echo "   ✅ strands-agents: $(pip list | grep strands-agents | awk '{print $2}')"
else
    echo "   ❌ strands-agents not found"
fi

if pip list | grep -q "bedrock-agentcore"; then
    echo "   ✅ bedrock-agentcore: $(pip list | grep bedrock-agentcore | awk '{print $2}')"
else
    echo "   ❌ bedrock-agentcore not found"
fi

if pip list | grep -q "streamlit"; then
    echo "   ✅ streamlit: $(pip list | grep streamlit | awk '{print $2}')"
else
    echo "   ❌ streamlit not found"
fi

# Check AWS credentials
echo "🔐 Checking AWS credentials..."
if aws sts get-caller-identity --profile CloudChef01 &> /dev/null; then
    account_id=$(aws sts get-caller-identity --profile CloudChef01 --query Account --output text)
    echo "   ✅ AWS CloudChef01 profile configured (Account: $account_id)"
else
    echo "   ❌ CloudChef01 profile not configured"
fi

echo ""
echo "✅ Environment ready! You can now run:"
echo "   python test_deployed_agent.py"
echo "   python test_tavily_agent.py"
echo "   cd streamlit_app && ./start_fast.sh"
echo ""
echo "💡 To activate manually: source venv/bin/activate"
