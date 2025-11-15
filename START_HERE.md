# 🚀 Quick Start - Dadd-E is Ready!

## ✅ What's Configured

- ✅ **Omi Glass**: MAC `9FFBF14A-4510-DFCE-A684-AB3362EE6B6A`
- ✅ **Wake Word**: "Daddy"
- ✅ **OpenAI**: Configured
- ✅ **Deepgram**: Configured (STT only)
- ✅ **Composio**: Configured
- ✅ **Supabase**: Configured

---

## 🎯 Start Dadd-E (2 Steps)

### Step 1: Start the Backend

Open a terminal and run:

```bash
./start_backend.sh
```

Or manually:

```bash
uv run main.py
```

**You should see:**
```
🚀 Starting Dadd-E
📡 Wake word: Daddy
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it:** Open http://localhost:8000/docs in your browser

---

### Step 2: Connect Your Omi Glasses

**In a NEW terminal**, run:

```bash
./start_device.sh
```

Or manually with conda (since omi-sdk needs Opus from conda):

```bash
# Make sure you're in conda environment
conda activate base

# Set library path
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/opus/lib:$DYLD_LIBRARY_PATH

# Run device runtime
python device/runtime.py
```

**You should see:**
```
🚀 Starting Dadd-E Runtime
📡 Backend: http://localhost:8000
🔌 Connecting to WebSocket...
✅ Connected to backend
```

---

## 🗣️ Test Voice Commands

Once both are running, try saying:

**"Daddy, what's in front of me?"**
- Analyzes the camera view

**"Daddy, check my Slack messages"**
- Retrieves Slack messages

**"Hey Daddy, search my Drive for proposal"**
- Searches Google Drive

---

## 🔧 Testing Before Connecting Glasses

You can test the backend without glasses:

### Test Wake Word Detection
```bash
curl "http://localhost:8000/voice/wake-word-test?text=hey%20daddy%20check%20slack"
```

Should return:
```json
{"text": "hey daddy check slack", "wake_word": "Daddy", "detected": true}
```

### Test Vision API
```bash
# Take a screenshot or use any image
curl -X POST "http://localhost:8000/vision/describe?user_id=test" \
  -F "image=@/path/to/image.jpg"
```

### Test App Integrations
First, connect your apps:
```bash
composio login
composio add slack
composio add gmail
composio add googledrive
```

---

## 📚 API Documentation

Once backend is running:
- **Interactive Docs**: http://localhost:8000/docs
- **API Info**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

---

## ⚠️ Known Issues

1. **Deepgram TTS not available** - Using v2.12.0 (omi-sdk requirement)
   - For voice responses, use OpenAI TTS instead
   - See `docs/KNOWN_ISSUES.md`

2. **Opus library** - Works in conda but not UV environment
   - Device runtime must run in conda environment
   - Backend can run in UV environment

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is already in use
lsof -ti:8000 | xargs kill -9

# Try again
uv run main.py
```

### Device runtime can't find Opus
```bash
# Run in conda environment
conda activate base

# Set library path
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/opus/lib:$DYLD_LIBRARY_PATH

# Try again
python device/runtime.py
```

### Can't connect to Omi glasses
```bash
# Rescan for devices
omi-scan

# Make sure Bluetooth is on
# Make sure glasses are powered on
# Check MAC address matches .env file
```

### Composio apps not working
```bash
# Check connected apps
composio apps

# Reconnect if needed
composio add slack
composio add gmail
composio add googledrive
```

---

## 📖 Documentation

- **Full README**: [README.md](README.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Deepgram Setup**: [docs/DEEPGRAM_SETUP.md](docs/DEEPGRAM_SETUP.md)
- **Known Issues**: [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md)

---

## 🎉 You're Ready!

1. Run `./start_backend.sh`
2. In new terminal, run `./start_device.sh`
3. Say "Daddy, what's in front of me?"
4. Build cool stuff! 🚀

---

**Need help?** Open an issue or check the docs!
