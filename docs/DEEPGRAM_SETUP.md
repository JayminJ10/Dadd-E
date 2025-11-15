# 🎙️ Deepgram Setup Guide for Dadd-E

## What is Deepgram?

Deepgram provides AI-powered voice APIs for your application:

1. **STT (Speech-to-Text)** ✅ - Converts what you say into text (we use this!)
2. **TTS (Text-to-Speech)** ⚠️ - Not available (SDK version conflict)
3. **Voice Agent API** - Full conversational AI (not needed for Dadd-E)

**Important Note:** We're using Deepgram SDK v2.12.0 (required by omi-sdk), which only supports STT. TTS requires v3+ which conflicts with omi-sdk. See [docs/KNOWN_ISSUES.md](KNOWN_ISSUES.md) for TTS alternatives (OpenAI TTS or ElevenLabs).

---

## 🚀 Getting Your Deepgram API Key

### Step 1: Create Account

1. Go to https://console.deepgram.com/
2. Sign up with your email (or GitHub/Google)
3. Verify your email

### Step 2: Get API Key

1. After login, you'll see the dashboard
2. Click on "API Keys" in the left sidebar
3. Click "Create a New API Key"
4. Give it a name (e.g., "Dadd-E")
5. **Copy the API key** - you won't see it again!

### Step 3: Add to Your .env File

```bash
# Open your .env file
nano .env

# Add your Deepgram API key
DEEPGRAM_API_KEY=YOUR_API_KEY_HERE
```

---

## 🎯 What Dadd-E Uses Deepgram For

### 1. STT - Speech-to-Text (Listening)

**When:** Every time you speak to your Omi glasses

**What it does:**
- Real-time transcription of your voice
- Wake word detection ("Dadd-e")
- Converts your commands to text

**Models we use:**
- `nova-2` - Latest and most accurate model
- Optimized for conversational speech
- Low latency for real-time response

### 2. TTS - Text-to-Speech (Speaking Back)

**When:** Dadd-E responds to your commands

**What it does:**
- Converts text responses to natural-sounding speech
- Plays audio back through your glasses/phone

**Voice options available:**

#### Female Voices
- `aura-asteria-en` - Default, warm and professional
- `aura-luna-en` - Friendly and conversational
- `aura-stella-en` - Clear and articulate
- `aura-athena-en` - Confident and authoritative
- `aura-hera-en` - Sophisticated and elegant

#### Male Voices
- `aura-orion-en` - Deep and authoritative
- `aura-arcas-en` - Warm and friendly
- `aura-perseus-en` - Professional and clear
- `aura-angus-en` - Casual and approachable
- `aura-orpheus-en` - Smooth and engaging
- `aura-helios-en` - Bright and energetic
- `aura-zeus-en` - Powerful and commanding

**To change the voice:**
```bash
# In your .env file
DEEPGRAM_TTS_VOICE=aura-luna-en  # Change to any voice above
```

---

## 💰 Pricing & Free Tier

### Free Credits
- $200 in free credits when you sign up
- No credit card required initially

### What You Get
- **STT:** ~45,000 minutes of transcription
- **TTS:** ~3.3M characters of speech generation

### Pay-As-You-Go Pricing
- **STT (Nova-2):** ~$0.0043/minute
- **TTS (Aura):** ~$0.015/1000 characters

For Dadd-E usage, the free tier should last you several months!

---

## 🧪 Testing Your Setup

### Test STT (Speech-to-Text)

```bash
# Make sure your backend is running
python main.py

# In another terminal, test wake word detection
curl "http://localhost:8000/voice/wake-word-test?text=hey%20dadd-e%20what%20is%20in%20front%20of%20me"

# Should return:
# {"text": "hey dadd-e what is in front of me", "wake_word": "dadd-e", "detected": true}
```

### Test TTS (Text-to-Speech)

```bash
# Test TTS endpoint
curl -X POST "http://localhost:8000/voice/text-to-speech?text=Hello,%20I%20am%20Dadd-E,%20your%20productivity%20assistant"

# Should return JSON with base64 encoded audio
```

Or test in the browser:
1. Go to http://localhost:8000/docs
2. Find the `/voice/text-to-speech` endpoint
3. Click "Try it out"
4. Enter some text
5. Execute and see the audio response

---

## 🔧 Advanced Configuration

### STT Options (in `app/services/voice.py`)

```python
options = LiveOptions(
    model="nova-2",              # Most accurate model
    language="en",               # Language
    smart_format=True,           # Auto formatting
    punctuate=True,              # Add punctuation
    interim_results=False,       # Only final results
    endpointing=300,             # Sentence detection
    utterance_end_ms=1000,       # Pause detection
)
```

### TTS Options (configurable in .env)

```env
# Voice selection
DEEPGRAM_TTS_VOICE=aura-asteria-en

# Model (matches the voice)
DEEPGRAM_TTS_MODEL=aura-asteria-en
```

---

## 🐛 Troubleshooting

### "Invalid API key" error
- Double-check your API key in `.env`
- Make sure there are no spaces or quotes around the key
- Verify the key is active in Deepgram console

### STT not transcribing
- Check your microphone permissions
- Verify Omi glasses are connected
- Look at backend logs for errors
- Test with: `curl http://localhost:8000/health`

### TTS returning errors
- Verify your API key has TTS access
- Check you have remaining credits
- Try a different voice model
- Look at the error message in logs

### Low quality transcription
- Ensure good audio quality from Omi glasses
- Check for background noise
- Verify you're using `nova-2` model
- Speak clearly and at normal pace

---

## 📚 Additional Resources

- [Deepgram Documentation](https://developers.deepgram.com/)
- [STT API Reference](https://developers.deepgram.com/reference/streaming)
- [TTS API Reference](https://developers.deepgram.com/reference/text-to-speech-api)
- [Voice Samples](https://developers.deepgram.com/docs/tts-models#aura)

---

## 🎯 Quick Reference

| Feature | What We Use | Purpose |
|---------|------------|---------|
| **STT Model** | `nova-2` | Most accurate transcription |
| **TTS Voice** | `aura-asteria-en` (default) | Natural-sounding responses |
| **Wake Word** | "dadd-e" (customizable) | Activation trigger |
| **Latency** | Real-time | Immediate responses |

---

**One API key, two powerful features - that's it!** 🎉

Get your key from https://console.deepgram.com/ and you're ready to go!
