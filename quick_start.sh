#!/bin/bash
cd /Users/mba/Desktop/strands-agentcore-app-20250917
source venv/bin/activate
nohup streamlit run streamlit_app/app_minimal_working.py --server.port 8501 > /dev/null 2>&1 &
echo "🚀 Streamlit app starting..."
echo "📱 Open: http://localhost:8501"
echo "🔍 Check if running: lsof -i :8501"
