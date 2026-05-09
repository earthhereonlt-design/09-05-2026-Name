# Instagram Username Finder Bot

Async Telegram bot that uses AI to generate and check Instagram username availability 24/7.

---

## Prerequisites

- Python 3.12+
- A Telegram bot token (from @BotFather)
- Your Telegram chat ID
- An OpenRouter API key (https://openrouter.ai)

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

## Getting Your Chat ID

1. Start a conversation with your bot
2. Send any message
3. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
4. Find "chat":{"id": XXXXXXX} — that's your TELEGRAM_CHAT_ID

---

## Railway Deployment

### 1. Push your code to GitHub

### 2. Go to https://railway.app → New Project → Deploy from GitHub Repo

### 3. Set Environment Variables in Railway dashboard:
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_CHAT_ID=...
   OPENROUTER_API_KEY=...
   OPENROUTER_MODEL=mistralai/mistral-7b-instruct

### 4. Railway will auto-detect the Dockerfile and deploy

### 5. Add a Volume in Railway:
   - Mount path: /app/data
   - This persists your SQLite database across restarts

### 6. After deploy, send /run to your bot in Telegram

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
