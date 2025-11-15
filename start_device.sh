#!/bin/bash
# Start Dadd-E Device Runtime (connects Omi glasses)

echo "🎧 Starting Dadd-E Device Runtime..."
echo ""
echo "📡 Connecting to Omi Glass: 9FFBF14A-4510-DFCE-A684-AB3362EE6B6A"
echo "🔊 Wake word: Daddy"
echo ""
echo "Make sure:"
echo "  1. Backend is running (run ./start_backend.sh in another terminal)"
echo "  2. Your Omi glasses are powered on and nearby"
echo "  3. Bluetooth is enabled"
echo ""
echo "Press CTRL+C to stop"
echo ""

# Set Opus library path (for macOS with Homebrew)
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/opus/lib:$DYLD_LIBRARY_PATH

# Start the device runtime
python device/runtime.py
