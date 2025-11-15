# Dadd-E 🤖

**Your real-time productivity assistant powered by Omi glasses**

Dadd-E is a Jarvis-like AI assistant that runs on Omi smart glasses, helping you stay productive by:
- 👀 Understanding what's in front of you
- 💬 Checking and responding to messages
- 📧 Sending emails and finding documents
- ✅ Creating tasks and managing your calendar
- 🎯 All hands-free, in real-time

## 🏗️ Architecture

```
Omi Glasses → Device Runtime → FastAPI Backend
                                    ↓
                ┌───────────────────┴───────────────────┐
                ↓                   ↓                   ↓
            Deepgram            OpenAI              Composio
            (Voice)          (Vision+LLM)    (Slack/Gmail/Drive)
                ↓                   ↓                   ↓
                └───────────────────┬───────────────────┘
                                    ↓
                                Supabase
                              (DB + Auth)
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.12+
- Omi DevKit glasses
- API Keys:
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Deepgram](https://console.deepgram.com/)
  - [Composio](https://app.composio.dev/)
  - [Supabase](https://supabase.com/)

### 2. Installation

```bash
# Clone and navigate to the project
cd Dadd-E

# Install dependencies using UV
uv sync

# Or using pip
pip install -e .
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Required:
# - OPENAI_API_KEY
# - DEEPGRAM_API_KEY
# - COMPOSIO_API_KEY
# - SUPABASE_URL
# - SUPABASE_KEY
# - OMI_DEVICE_MAC
```

### 4. Set Up Supabase

1. Create a new Supabase project
2. Go to SQL Editor
3. Run the `database_schema.sql` file
4. Copy your project URL and API keys to `.env`

### 5. Connect Your Apps

```bash
# Install Composio CLI
pip install composio-core

# Connect your apps (Slack, Gmail, Drive, etc.)
composio login
composio add slack
composio add gmail
composio add googledrive
```

### 6. Run the Backend

```bash
# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Connect Your Omi Glasses

```bash
# In a new terminal
# First, find your Omi device MAC address
omi-scan

# Add the MAC address to your .env file
# OMI_DEVICE_MAC=XX:XX:XX:XX:XX:XX

# Run the device runtime
python device/runtime.py
```

## 💡 Usage Examples

### Basic Voice Commands

**"Dadd-e, what's in front of me?"**
- Analyzes the camera view and describes the scene

**"Dadd-e, check my Slack messages in general"**
- Retrieves recent messages from your Slack #general channel

**"Dadd-e, send an email to sai@example.com about the proposal"**
- Composes and sends an email

### Complex Multi-Step Tasks

**"Hey Dadd-e, check my Slack for messages from Sai about the proposal, find the proposal doc in Google Drive, and email it to him"**

Dadd-E will:
1. ✅ Check Slack for messages from Sai
2. 🔍 Search Google Drive for "proposal"
3. 📧 Send email with the document to Sai

## 🛠️ API Endpoints

### Voice
- `WS /voice/transcribe` - Real-time audio transcription (STT)
- `POST /voice/wake-word-test` - Test wake word detection
- `POST /voice/text-to-speech` - Convert text to speech (TTS)

### Vision
- `POST /vision/analyze` - Analyze image with custom prompt
- `POST /vision/describe` - Get scene description
- `POST /vision/read-text` - Extract text from image (OCR)

### Actions
- `POST /actions/execute` - Execute single action
- `POST /actions/complex-task` - Execute multi-step task
- `GET /actions/connected-apps` - Get connected app list

### Health
- `GET /` - API info
- `GET /health` - Health check

## 📁 Project Structure

```
Dadd-E/
├── app/
│   ├── core/           # Configuration
│   ├── models/         # Pydantic schemas
│   ├── routers/        # API endpoints
│   ├── services/       # Business logic
│   │   ├── voice.py        # Deepgram integration
│   │   ├── vision.py       # OpenAI vision + LLM
│   │   ├── integrations.py # Composio app connections
│   │   └── database.py     # Supabase client
│   └── main.py         # FastAPI app
├── device/
│   ├── omi_service.py  # Omi glasses integration
│   └── runtime.py      # Device runtime
├── .env.example        # Environment template
├── database_schema.sql # Supabase schema
└── pyproject.toml      # Dependencies
```

## 🔧 Development

### Install Dev Dependencies

```bash
uv sync --dev

# Or with pip
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code
black app/ device/

# Lint
ruff check app/ device/
```

## 🌐 Deployment

### Railway (Recommended)

1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Deploy!

Railway will auto-detect FastAPI and deploy with:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Docker (Alternative)

```bash
# Build image
docker build -t dadd-e .

# Run container
docker run -p 8000:8000 --env-file .env dadd-e
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License

## 🙏 Acknowledgments

- [Omi](https://github.com/BasedHardware/omi) - Open-source AI wearable
- [Deepgram](https://deepgram.com/) - Real-time voice transcription
- [OpenAI](https://openai.com/) - Vision and language models
- [Composio](https://composio.dev/) - App integrations
- [Supabase](https://supabase.com/) - Database and auth

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check the [Omi Discord](https://discord.gg/omi)

---

Built with ❤️ for productivity 
