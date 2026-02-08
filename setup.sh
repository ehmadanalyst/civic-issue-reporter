#!/bin/bash

echo "🌟 Civic Issue Reporter - Quick Setup Script"
echo "=============================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Ask which version to use
echo "Which AI API do you want to use?"
echo "1) Gemini API (recommended - free tier)"
echo "2) Claude API (premium)"
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "📦 Installing dependencies for Gemini..."
    pip3 install -r requirements_gemini.txt
    
    echo ""
    echo "🔑 Please enter your Google API Key"
    echo "Get it from: https://aistudio.google.com/apikey"
    read -p "API Key: " api_key
    
    export GOOGLE_API_KEY="$api_key"
    
    echo ""
    echo "✅ Setup complete!"
    echo "🚀 Starting server with Gemini API..."
    python3 backend_api_gemini.py
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "📦 Installing dependencies for Claude..."
    pip3 install -r requirements.txt
    
    echo ""
    echo "🔑 Please enter your Anthropic API Key"
    echo "Get it from: https://console.anthropic.com/"
    read -p "API Key: " api_key
    
    export ANTHROPIC_API_KEY="$api_key"
    
    echo ""
    echo "✅ Setup complete!"
    echo "🚀 Starting server with Claude API..."
    python3 backend_api.py
    
else
    echo "❌ Invalid choice. Please run again and select 1 or 2."
    exit 1
fi
