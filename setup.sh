#!/bin/bash

# HelloWorld Strands Agent Setup Script

echo "🚀 HelloWorld Strands Agent Setup"
echo "=================================="

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "   $python_version"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    echo "❌ Python 3.10+ is required"
    exit 1
fi

# Check AWS CLI
echo "🔍 Checking AWS CLI..."
if command -v aws &> /dev/null; then
    aws_version=$(aws --version 2>&1)
    echo "   $aws_version"
else
    echo "❌ AWS CLI not found. Please install AWS CLI first."
    exit 1
fi

# Check AWS credentials
echo "🔍 Checking AWS credentials..."
if aws sts get-caller-identity --profile CloudChef01 &> /dev/null; then
    account_id=$(aws sts get-caller-identity --profile CloudChef01 --query Account --output text)
    echo "   ✅ AWS credentials configured for CloudChef01 profile (Account: $account_id)"
else
    echo "❌ CloudChef01 profile not configured. Please set up the profile first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if pip3 install -r requirements.txt; then
    echo "   ✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Make scripts executable
chmod +x test_agent.py
chmod +x deploy_agentcore.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Start the agent locally:"
echo "      python3 agent.py"
echo ""
echo "   2. In another terminal, test the agent:"
echo "      python3 test_agent.py"
echo ""
echo "   3. Deploy to AgentCore (optional):"
echo "      python3 deploy_agentcore.py"
echo ""
echo "📚 See README.md for detailed instructions"
