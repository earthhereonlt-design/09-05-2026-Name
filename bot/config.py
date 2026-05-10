"""
Centralized environment variable configuration with validation.
Required env vars: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GEMINI_API_KEY
"""

import os
import sys
from bot.utils.helpers import log


class Config:
    # ─── REQUIRED ───────────────────────────────────────────────────────
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

    # ─── OPTIONAL (with sensible defaults) ──────────────────────────────
    GEMINI_MODEL = "gemini-2.0-flash"
    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    # ─── ADVANCED TUNING (rarely need to change) ────────────────────────
    RATE_LIMIT_COOLDOWN = int(os.getenv("RATE_LIMIT_COOLDOWN", "60"))  # seconds
    BATCH_DELAY = float(os.getenv("BATCH_DELAY", "3.0"))  # between batches
    CHECK_DELAY_MIN = float(os.getenv("CHECK_DELAY_MIN", "2.5"))
    CHECK_DELAY_MAX = float(os.getenv("CHECK_DELAY_MAX", "5.0"))
    MESSAGE_DELETE_TIMEOUT = int(os.getenv("MESSAGE_DELETE_TIMEOUT", "30"))  # seconds

    @staticmethod
    def validate() -> bool:
        """Validate all required environment variables are set."""
        errors = []

        if not Config.TELEGRAM_BOT_TOKEN:
            errors.append("❌ TELEGRAM_BOT_TOKEN not set")
        elif len(Config.TELEGRAM_BOT_TOKEN) < 20:
            errors.append("❌ TELEGRAM_BOT_TOKEN looks invalid (too short)")

        if not Config.TELEGRAM_CHAT_ID:
            errors.append("❌ TELEGRAM_CHAT_ID not set")
        else:
            try:
                int(Config.TELEGRAM_CHAT_ID)
            except ValueError:
                errors.append("❌ TELEGRAM_CHAT_ID must be a number")

        if not Config.GEMINI_API_KEY:
            errors.append("❌ GEMINI_API_KEY not set")
        elif len(Config.GEMINI_API_KEY) < 10:
            errors.append("❌ GEMINI_API_KEY looks invalid (too short)")

        if errors:
            print("\n🚨 CONFIGURATION ERROR 🚨\n")
            for err in errors:
                print(err)
            print("\n📝 Set these environment variables:\n")
            print("  TELEGRAM_BOT_TOKEN=your_bot_token_here")
            print("  TELEGRAM_CHAT_ID=your_chat_id_here")
            print("  GEMINI_API_KEY=your_gemini_api_key_here")
            print("\n(Get Gemini API key from: https://aistudio.google.com/apikey)\n")
            return False
        return True
