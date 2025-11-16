#!/bin/bash
# Quick script to connect Omi device to backend

echo "🎧 Connecting Omi Glass to Dadd-E Backend..."
echo ""
echo "Make sure:"
echo "  ✅ Backend is running (uv run main.py in another terminal)"
echo "  ✅ Omi glasses are powered on and nearby"
echo "  ✅ Bluetooth is enabled"
echo ""
echo "Device MAC: 9FFBF14A-4510-DFCE-A684-AB3362EE6B6A"
echo "Backend: http://localhost:8000"
echo "Wake word: Daddy"
echo ""
echo "Press CTRL+C to stop"
echo ""

# Set Opus library path
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/opus/lib:$DYLD_LIBRARY_PATH

# Run device runtime
python device/runtime.py
