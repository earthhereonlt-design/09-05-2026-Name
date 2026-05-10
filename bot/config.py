"""
Centralized environment variable configuration with validation.
Only 3 required env vars: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, OPENROUTER_API_KEY
"""

import os
import sys
from bot.utils.helpers import log


class Config:
    # ─── REQUIRED ───────────────────────────────────────────────────────
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()

    # ─── OPTIONAL (with sensible defaults) ──────────────────────────────
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct").strip()
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

    # ─── ADVANCED TUNING (rarely need to change) ────────────────────────
    RATE_LIMIT_COOLDOWN = int(os.getenv("RATE_LIMIT_COOLDOWN", "60"))  # seconds
    BATCH_DELAY = float(os.getenv("BATCH_DELAY", "3.0"))  # between batches
    CHECK_DELAY_MIN = float(os.getenv("CHECK_DELAY_MIN", "2.5"))
    CHECK_DELAY_MAX = float(os.getenv("CHECK_DELAY_MAX", "5.0"))

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

        if not Config.OPENROUTER_API_KEY:
            errors.append("❌ OPENROUTER_API_KEY not set")
        elif len(Config.OPENROUTER_API_KEY) < 10:
            errors.append("❌ OPENROUTER_API_KEY looks invalid (too short)")

        if errors:
            print("\n🚨 CONFIGURATION ERROR 🚨\n")
            for err in errors:
                print(err)
            print("\n📝 Set these environment variables:\n")
            print("  TELEGRAM_BOT_TOKEN=your_bot_token_here")
            print("  TELEGRAM_CHAT_ID=your_chat_id_here")
            print("  OPENROUTER_API_KEY=your_api_key_here")
            print("\n(OPENROUTER_MODEL is optional, defaults to mistral-7b)\n")
            return False
        return True
