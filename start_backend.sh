#!/bin/bash
# Start Dadd-E Backend

echo "🚀 Starting Dadd-E Backend..."
echo ""
echo "📡 Backend will be available at: http://localhost:8000"
echo "📖 API docs at: http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop"
echo ""

# Set Opus library path (for macOS with Homebrew)
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/opus/lib:$DYLD_LIBRARY_PATH

# Start the backend
uv run main.py
