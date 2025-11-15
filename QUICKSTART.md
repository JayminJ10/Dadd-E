# 🚀 Dadd-E Quick Start Guide

## Step-by-Step Setup

### 1️⃣ Install Dependencies

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -e .
```

### 2️⃣ Get Your API Keys

You'll need API keys from these services:

1. **OpenAI** - https://platform.openai.com/api-keys
   - Used for vision analysis and LLM reasoning
   - GPT-4o model access required

2. **Deepgram** - https://console.deepgram.com/
   - Used for STT (Speech-to-Text) and TTS (Text-to-Speech)
   - Same API key works for both!
   - Free tier: $200 credits
   - 📖 See [docs/DEEPGRAM_SETUP.md](docs/DEEPGRAM_SETUP.md) for detailed setup

3. **Composio** - https://app.composio.dev/
   - Used for app integrations (Slack, Gmail, Drive)
   - Sign up and get API key

4. **Supabase** - https://supabase.com/
   - Used for database and authentication
   - Create a new project

### 3️⃣ Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and fill in your API keys
nano .env  # or use your preferred editor
```

Required environment variables:
```env
OPENAI_API_KEY=sk-...
DEEPGRAM_API_KEY=...
COMPOSIO_API_KEY=...
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...
```

### 4️⃣ Set Up Supabase Database

1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Copy the contents of `database_schema.sql`
4. Paste and run it in the SQL editor
5. Verify tables were created in the Table Editor

### 5️⃣ Connect Your Apps via Composio

```bash
# Login to Composio
composio login

# Connect Slack
composio add slack

# Connect Gmail
composio add gmail

# Connect Google Drive
composio add googledrive

# (Optional) Connect other apps
composio add notion
composio add googlecalendar
```

### 6️⃣ Find Your Omi Device

```bash
# Scan for Bluetooth devices
omi-scan

# Look for a device named "Omi" or similar
# Copy its MAC address (e.g., 7F:52:EC:55:50:C9)

# Add to .env
echo "OMI_DEVICE_MAC=YOUR_MAC_ADDRESS" >> .env
```

### 7️⃣ Start the Backend

```bash
# Option 1: Using the main.py entry point
python main.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# You should see:
# 🚀 Starting Dadd-E
# 📡 Wake word: dadd-e
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 8️⃣ Test the Backend

Open your browser and go to:
- http://localhost:8000 - API info
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/health - Health check

Test the voice features:
```bash
# Test wake word detection
curl "http://localhost:8000/voice/wake-word-test?text=hey%20daddy%20check%20slack"

# Test text-to-speech
curl -X POST "http://localhost:8000/voice/text-to-speech?text=Hello,%20I%20am%20Dadd-E"
```

### 9️⃣ Connect Your Omi Glasses

In a **new terminal**:

```bash
# Run the device runtime
python device/runtime.py

# You should see:
# 🚀 Starting Dadd-E Runtime
# 📡 Backend: http://localhost:8000
# 🔌 Connecting to WebSocket...
# ✅ Connected to backend
```

### 🔟 Test Voice Commands

With your Omi glasses connected and the backend running:

1. Say: **"Dadd-e, what's in front of me?"**
   - The glasses will capture an image and describe what you see

2. Say: **"Dadd-e, check my Slack messages"**
   - It will retrieve your recent Slack messages

3. Say: **"Dadd-e, search my Drive for proposal"**
   - It will search Google Drive for files matching "proposal"

## 🎯 Common Commands

### Scene Understanding
- "Dadd-e, what do you see?"
- "Dadd-e, read the text in front of me"
- "Dadd-e, describe this"

### Slack
- "Dadd-e, check my Slack in #general"
- "Dadd-e, any messages from [person]?"

### Email
- "Dadd-e, send an email to person@example.com about the meeting"

### Google Drive
- "Dadd-e, find my presentation deck"
- "Dadd-e, search for quarterly report"

### Complex Tasks
- "Dadd-e, check Slack for messages from Sai, find the doc he mentioned, and email it to him"

## 🐛 Troubleshooting

### Backend won't start
- Check if all environment variables are set
- Verify API keys are valid
- Make sure port 8000 is not in use

### Can't connect to Omi device
- Verify Bluetooth is enabled
- Check the MAC address is correct
- Try running `omi-scan` again
- Make sure the device is powered on and nearby

### Composio integrations not working
- Run `composio apps` to see connected apps
- Reconnect apps if needed: `composio add [app-name]`
- Check that you're logged in: `composio whoami`

### Deepgram transcription issues
- Verify your API key is correct
- Check your Deepgram account credits
- Try the wake word test: `curl http://localhost:8000/voice/wake-word-test?text=hey%20dadd-e`

### Database errors
- Ensure Supabase schema was created successfully
- Check your Supabase project is active
- Verify the SUPABASE_URL and keys are correct

## 📚 Next Steps

1. **Customize wake word** - Change `WAKE_WORD` in `.env`
2. **Add more apps** - Connect additional services via Composio
3. **Deploy to Railway** - Host your backend in the cloud
4. **Create custom intents** - Modify `app/services/vision.py` to add new command types

## 💡 Tips

- Keep the backend terminal open to see real-time logs
- Use the FastAPI docs (http://localhost:8000/docs) to test endpoints manually
- Check Supabase dashboard to see logged actions and vision analyses
- Start with simple commands before trying complex multi-step tasks

---

Need help? Check the main README.md or open an issue!
