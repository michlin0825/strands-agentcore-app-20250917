#!/bin/bash

# Strands AgentCore App - Environment-based Startup Script

echo "🚀 Starting Strands AgentCore App (Environment-based)"
echo "=================================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your values:"
    echo "cp .env.example .env"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Error: Virtual environment not found!"
    echo "Please create virtual environment: python -m venv venv"
    exit 1
fi

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check required environment variables
echo "🔍 Checking environment variables..."
source .env

if [ -z "$AGENT_RUNTIME_ARN" ]; then
    echo "❌ Error: AGENT_RUNTIME_ARN not set in .env file"
    exit 1
fi

if [ -z "$AWS_REGION" ]; then
    echo "❌ Error: AWS_REGION not set in .env file"
    exit 1
fi

echo "✅ Environment variables configured:"
echo "   AWS_PROFILE: ${AWS_PROFILE:-Default}"
echo "   AWS_REGION: $AWS_REGION"
echo "   KNOWLEDGE_BASE_ID: ${KNOWLEDGE_BASE_ID:-Not set}"

# Start the application
echo "🌟 Starting Streamlit app..."
echo "App will be available at: http://localhost:8503"
echo "Press Ctrl+C to stop"

streamlit run streamlit_app/app_env.py --server.port 8503
