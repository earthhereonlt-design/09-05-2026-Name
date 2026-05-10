# 🚀 Deployment Guide - Instagram Username Bot

## Quick Start (Railway.app)

### Step 1: Get Your Credentials

#### 🤖 Telegram Bot Token
1. Open Telegram and message **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy your bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 📌 Telegram Chat ID
1. Add your bot to a Telegram chat (DM or group)
2. Send `/start` to the bot
3. The chat ID will be logged (it's just a number like `123456789`)

#### 🔑 OpenRouter API Key
1. Go to https://openrouter.ai/keys
2. Sign up / Log in
3. Create an API key
4. Copy it (looks like: `sk-or-...`)

---

### Step 2: Deploy on Railway

1. **Push to GitHub** (if not already)
   ```bash
   git push origin main
   ```

2. **Connect Railway to your repo**
   - Go to https://railway.app/dashboard
   - Click "New Project" → "Deploy from GitHub"
   - Select your repo

3. **Set Environment Variables**
   
   In Railway dashboard, go to **Variables** and add ONLY these 3:

   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   OPENROUTER_API_KEY=your_api_key_here
   ```

   **Optional** (leave empty or remove if using defaults):
   - `OPENROUTER_MODEL=mistralai/mistral-7b-instruct`

4. **Click Deploy** ✅

---

## 📊 Environment Variables Explained

### Required (3 only)
| Variable | What is it? | Where to get |
|----------|-----------|--------------|
| `TELEGRAM_BOT_TOKEN` | Your bot's authentication token | @BotFather on Telegram |
| `TELEGRAM_CHAT_ID` | Chat where bot sends messages | Send /start to bot, check logs |
| `OPENROUTER_API_KEY` | API key for AI model access | https://openrouter.ai/keys |

### Optional (don't need to set - already have good defaults)
| Variable | Default | What does it do |
|----------|---------|-----------------|
| `OPENROUTER_MODEL` | `mistralai/mistral-7b-instruct` | Which AI model to use |
| `RATE_LIMIT_COOLDOWN` | `60` | Seconds to wait after Instagram rate limits |
| `BATCH_DELAY` | `3.0` | Seconds between username batches |
| `CHECK_DELAY_MIN` | `2.5` | Min seconds between checks |
| `CHECK_DELAY_MAX` | `5.0` | Max seconds between checks |

---

## 🔧 Troubleshooting

### ❌ Bot not responding?
1. Check Railway logs: Dashboard → Your Project → Logs
2. Look for "Configuration Error" - means env vars missing
3. Verify all 3 required variables are set correctly

### ❌ "OPENROUTER_API_KEY not set" error?
- Make sure you copied the full key from https://openrouter.ai/keys
- Remove any extra spaces or newlines

### ❌ "TELEGRAM_BOT_TOKEN looks invalid"?
- Get a new token from @BotFather
- Make sure it's the full token (format: `123456:ABC...`)

### ❌ "TELEGRAM_CHAT_ID must be a number"?
- Chat ID is just digits, no special characters
- Get it by sending `/start` to your bot and checking logs

---

## 📝 Local Testing

Before deploying, test locally:

1. Create `.env` file (copy from `.env.example`)
2. Fill in your 3 credentials
3. Run: `python -m bot.main`
4. Check for errors

---

## 🆘 Still having issues?

1. Check Railway logs for the exact error
2. Verify env variables match examples exactly (no extra spaces)
3. Ensure all 3 required variables are set
4. Restart the Railway deployment after fixing variables
