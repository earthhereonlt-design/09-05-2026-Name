# Instagram Username Finder Bot

Async Telegram bot that uses Google's Gemini AI to generate and check Instagram username availability 24/7.

---

## 🚀 Quick Deployment

**Only need 3 environment variables:**
- `TELEGRAM_BOT_TOKEN` — Get from @BotFather
- `TELEGRAM_CHAT_ID` — Your Telegram chat ID  
- `GEMINI_API_KEY` — Get from https://aistudio.google.com/apikey

**See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.**

---

## Prerequisites

- Python 3.12+
- A Telegram bot token (from @BotFather)
- Your Telegram chat ID
- A Google Gemini API key (https://aistudio.google.com/apikey)

---

## Local Setup

### 1. Clone and enter the project
git clone <your-repo>
cd instagram-username-bot

### 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Install Playwright browser
playwright install chromium

### 5. Set up environment variables
cp .env.example .env
# Edit .env with your actual values

### 6. Run the bot
python -m bot.main

### 7. In Telegram, send:
/run

---

---

## Getting Your Chat ID

1. Start a conversation with your bot
2. Send any message
3. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
4. Find "chat":{"id": XXXXXXX} — that's your TELEGRAM_CHAT_ID

---

## Environment Variables

**Required (3):**
- `TELEGRAM_BOT_TOKEN` — Telegram bot token
- `TELEGRAM_CHAT_ID` — Your Telegram chat ID
- `OPENROUTER_API_KEY` — OpenRouter API key

**Optional (have sensible defaults):**
- `OPENROUTER_MODEL` — AI model (default: mistral-7b)
- `RATE_LIMIT_COOLDOWN` — Cooldown after rate limit (default: 60s)
- `BATCH_DELAY` — Delay between batches (default: 3s)
- `CHECK_DELAY_MIN/MAX` — Delay between checks (default: 2.5-5s)

---

## Railway Deployment

1. Push code to GitHub
2. Go to https://railway.app → "New Project" → "Deploy from GitHub"
3. Add 3 required environment variables
4. Create a volume at `/app/data` for persistence
5. Deploy!

**See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions with screenshots.**

---

## Architecture

- **aiogram v3** — async Telegram bot framework
- **Playwright** — headless browser fallback for Instagram checks
- **httpx** — lightweight async HTTP for primary checks
- **OpenRouter** — AI username generation via any LLM
- **aiosqlite** — async SQLite for persistence
- **asyncio** — fully async, single-threaded event loop

---

## How It Works

1. Bot receives /run command
2. Runner calls OpenRouter AI → gets 25 username suggestions
3. Each username is checked on Instagram:
   - Fast HTTP check first
   - Playwright fallback if HTTP is inconclusive
4. Available usernames are sent as Telegram messages
5. A single live progress message is edited repeatedly (no spam)
6. On Railway restart, bot auto-resumes from last state
7. All results stored in SQLite with full logs

---

## Tuning

| Env Variable         | Default | Description                        |
|----------------------|---------|------------------------------------|
| RATE_LIMIT_COOLDOWN  | 60      | Seconds to wait after rate limit   |
| BATCH_DELAY          | 3.0     | Seconds between batches            |
| CHECK_DELAY_MIN      | 2.5     | Min delay between individual checks|
| CHECK_DELAY_MAX      | 5.0     | Max delay between individual checks|

---

## Commands

| Command   | Description                                      |
|-----------|--------------------------------------------------|
| /run      | Start the infinite generate → check loop         |
| /stop     | Gracefully stop the loop                         |
| /status   | Current username, totals, runtime                |
| /log      | Last 5 log entries                               |
| /export   | Download available usernames as .txt             |
| /clear    | Clear stats and logs (keeps found usernames)     |
| /help     | List all commands                                |
