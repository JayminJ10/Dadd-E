# Known Issues & Limitations

## 🎙️ Deepgram TTS Not Available

**Issue:** Text-to-Speech (TTS) is not available in the current setup.

**Why:**
- `omi-sdk` requires `deepgram-sdk==2.12.0` (v2)
- Deepgram TTS was only added in `deepgram-sdk>=3.0.0` (v3)
- These versions have incompatible APIs

**Workarounds:**

### Option 1: Use OpenAI TTS (Recommended)

Add OpenAI TTS to `app/services/voice.py`:

```python
from openai import AsyncOpenAI

async def text_to_speech_openai(self, text: str) -> bytes:
    """Use OpenAI TTS instead of Deepgram"""
    settings = get_settings()
    client = AsyncOpenAI(api_key=settings.openai_api_key)

    response = await client.audio.speech.create(
        model="tts-1",
        voice="nova",  # alloy, echo, fable, onyx, nova, shimmer
        input=text
    )

    return response.content
```

### Option 2: Use ElevenLabs

```bash
uv add elevenlabs
```

Then add to `app/services/voice.py`:

```python
from elevenlabs import generate, set_api_key

def text_to_speech_elevenlabs(self, text: str) -> bytes:
    """Use ElevenLabs TTS"""
    settings = get_settings()
    set_api_key(settings.elevenlabs_api_key)

    audio = generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    return audio
```

### Option 3: Wait for omi-sdk Update

Monitor https://github.com/BasedHardware/omi for updates that support Deepgram SDK v3+.

---

## 📦 aiohttp Warning

**Warning:** `aiohttp==3.11.14` is yanked due to regression.

**Impact:** Minimal - the regression doesn't affect our use case.

**Fix:** Will be resolved when omi-sdk updates its dependencies.

---

## 🔧 Opus Library on macOS

**Issue:** `omi-scan` fails with "Could not find Opus library"

**Fix:**

1. Install Opus:
   ```bash
   brew install opus
   ```

2. Set library path (if using conda):
   ```bash
   export DYLD_LIBRARY_PATH=/opt/homebrew/opt/opus/lib:$DYLD_LIBRARY_PATH
   ```

3. Or install in conda:
   ```bash
   conda install -c conda-forge opus libopus
   ```

---

## 🐛 Reporting Issues

Found a bug? Open an issue on GitHub with:
- Error message
- Steps to reproduce
- Your environment (OS, Python version)
- Output of `uv run python --version`
