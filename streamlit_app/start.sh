#!/bin/bash
echo "🚀 Starting HelloWorld Strands Agent..."
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
streamlit run app.py --server.port 8501 2>/dev/null
