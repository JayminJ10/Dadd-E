# 🚂 Railway Deployment Guide

Deploy Dadd-E backend to Railway in minutes!

---

## 📋 Prerequisites

1. A [Railway](https://railway.app/) account (free tier available)
2. Your Dadd-E project pushed to GitHub
3. API keys ready (OpenAI, Deepgram, Composio, Supabase)

---

## 🚀 Deploy to Railway

### Step 1: Create New Project

1. Go to [railway.app](https://railway.app/)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `Dadd-E` repository
5. Railway will auto-detect it as a Python app

### Step 2: Configure Environment Variables

In your Railway project dashboard:

1. Click on your service
2. Go to **"Variables"** tab
3. Add **"Add Variable"** → **"Add Reference"** and add these:

```bash
# Required API Keys
OPENAI_API_KEY=sk-...
DEEPGRAM_API_KEY=...
COMPOSIO_API_KEY=...

# Supabase
SUPABASE_URL=https://....supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...

# Redis (Railway provides this)
REDIS_URL=${REDIS_URL}

# Application Settings
APP_NAME=Dadd-E
DEBUG=False
HOST=0.0.0.0
PORT=${PORT}

# Wake Word
WAKE_WORD=Daddy

# Models
OPENAI_MODEL=gpt-4o
VISION_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-large

# Feature Flags
ENABLE_VISION=True
ENABLE_VOICE_STT=True
ENABLE_VOICE_TTS=False
ENABLE_APP_INTEGRATIONS=True
```

**Note:** Railway automatically provides `PORT` and `REDIS_URL` variables.

### Step 3: Add Redis (Optional but Recommended)

1. In your Railway project, click **"New"**
2. Select **"Database"** → **"Add Redis"**
3. Railway will auto-link it to your service

### Step 4: Deploy

1. Railway will automatically deploy on push
2. Wait for the build to complete (~2-3 minutes)
3. Get your deployment URL (e.g., `https://dadd-e.railway.app`)

---

## 🔗 Connect Your Omi Glasses to Railway

### Update Your Local .env

```bash
# Change BACKEND_URL to your Railway URL
BACKEND_URL=https://your-app.railway.app

# Keep other settings
USER_ID=test_user
OMI_DEVICE_MAC=9FFBF14A-4510-DFCE-A684-AB3362EE6B6A
```

### Test Connection

```bash
# Test the deployed backend
curl https://your-app.railway.app/health

# Should return: {"status":"healthy","app":"Dadd-E"}
```

### Connect Omi Glasses

```bash
# In conda environment (for Opus library)
conda activate base

# Set library path
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/opus/lib:$DYLD_LIBRARY_PATH

# Run device runtime (it will use BACKEND_URL from .env)
python device/runtime.py
```

**You should see:**
```
🚀 Starting Dadd-E Runtime
📡 Backend: https://your-app.railway.app
👤 User ID: test_user
🎧 Device MAC: 9FFBF14A-4510-DFCE-A684-AB3362EE6B6A
🔌 Connecting to WebSocket: wss://your-app.railway.app/voice/transcribe
✅ Connected to backend
```

---

## ✅ Verify Deployment

### Check Health
```bash
curl https://your-app.railway.app/health
```

### Check API Docs
Open in browser: `https://your-app.railway.app/docs`

### Test Wake Word
```bash
curl "https://your-app.railway.app/voice/wake-word-test?text=hey%20daddy%20check%20slack"
```

---

## 🔧 Railway Configuration Files

Railway auto-detects these files:

### `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `Procfile`
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 📊 Monitoring

### View Logs

In Railway dashboard:
1. Click your service
2. Go to **"Deployments"**
3. Click on latest deployment
4. View live logs

### Metrics

Railway provides:
- CPU usage
- Memory usage
- Network traffic
- Response times

---

## 💰 Pricing

### Free Tier
- $5 of usage per month
- Good for development and testing
- Auto-sleep after inactivity

### Hobby Plan ($5/month)
- $5 credit + pay for what you use
- No auto-sleep
- Custom domains
- Better for production

### Estimated Costs

For Dadd-E:
- **Backend**: ~$3-5/month (always on)
- **Redis**: ~$1-2/month (if used)
- **Total**: ~$4-7/month

---

## 🐛 Troubleshooting

### Build Fails

**Check Python version:**
```bash
# Railway uses Python 3.11 by default
# Make sure pyproject.toml allows it
requires-python = ">=3.11"
```

**Check logs:**
Look for missing dependencies or import errors in build logs.

### WebSocket Connection Fails

**Check CORS settings:**
Make sure `app/main.py` allows your domain:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Test WebSocket:**
```bash
# Use wscat to test
npm install -g wscat
wscat -c wss://your-app.railway.app/voice/transcribe?user_id=test
```

### High Response Times

**Check region:**
- Railway deploys to US by default
- If you're far away, expect higher latency
- Consider deploying closer to your location

**Enable Redis caching:**
Add Redis database to improve performance.

---

## 🔒 Security Best Practices

### 1. Use Environment Variables
Never commit API keys to GitHub!

### 2. Disable Debug Mode
```bash
DEBUG=False
```

### 3. Use Service Keys
Use Supabase service role key for backend operations.

### 4. Enable Rate Limiting
Add rate limiting middleware (optional):
```bash
pip install slowapi
```

### 5. Monitor Usage
Check Railway metrics regularly for unusual activity.

---

## 🚀 Deployment Workflow

### Local Development
```bash
# Test locally
uv run main.py
```

### Push to Deploy
```bash
git add .
git commit -m "Update Dadd-E"
git push origin main
```

Railway auto-deploys on push to main branch!

### Rollback if Needed
In Railway dashboard:
1. Go to **"Deployments"**
2. Click previous working deployment
3. Click **"Redeploy"**

---

## 📚 Resources

- [Railway Docs](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app/)

---

## ✨ Next Steps

1. **Set up custom domain** (Railway Pro)
2. **Add monitoring** (Sentry, LogRocket)
3. **Set up CI/CD** (GitHub Actions)
4. **Add rate limiting** (SlowAPI)
5. **Enable HTTPS only** (Railway handles this automatically)

---

**Deployed and ready!** 🎉

Your Omi glasses can now connect from anywhere with internet!
