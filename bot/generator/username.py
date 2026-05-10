import json
import asyncio
import httpx
from bot.database import db
from bot.utils.helpers import log
from bot.config import Config

GEMINI_API_KEY = Config.GEMINI_API_KEY
GEMINI_URL = Config.GEMINI_URL

# Pattern variations provided by user
DOT_SUFFIXES = [
    "ai", "ml", "vr", "xr", "db", "ui", "ux", "os", "gg", "ff", 
    "tt", "dev", "it", "cc", "tv", "rx", "tx", "dx", "cx", "pk", 
    "kz", "jp", "kr", "uk", "us", "in", "qa", "id", "am", "io",
    "co", "me", "tv", "app", "web"
]

UNDERSCORE_SUFFIXES = [
    "ai", "ml", "vr", "xr", "db", "ui", "ux", "os", "rx", "tx",
    "dx", "cx", "pk", "jp", "kr", "uk", "us", "in", "id", "am",
    "bot", "dev", "app", "pro", "lab"
]

BASES = ["aadi", "adi", "aa", "ad"]

SYSTEM_PROMPT = """You are a username generator for Instagram usernames in the format of:
- base (aadi, adi, aa, ad) + dot + suffix (ai, ml, dev, io, etc.)
- base + underscore + suffix
- base + 2 letter country codes (us, uk, in, jp, etc.)

Examples: aadi.ai, aadi_ml, adi.dev, aa.io, ad_px

Generate ONLY usernames following these patterns. Return ONLY a valid JSON array of 30 unique strings. No explanations."""

async def generate_usernames(used: set[str]) -> list[str]:
    """Call Gemini API and return 30 fresh usernames."""
    used_sample = list(used)[-30:] if len(used) > 30 else list(used)
    
    user_prompt = f"""Generate 30 unique Instagram usernames using patterns like:
- aadi.ai, aadi.ml, aadi.dev, adi.io, aa.co, ad.tv
- aadi_ai, aadi_ml, adi_dev, aa_px, ad_us

Skip these (already checked): {', '.join(used_sample) if used_sample else 'none'}

Return ONLY a valid JSON array of 30 strings. Example: ["aadi.ai", "adi_ml", "aa.dev", ...]"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_prompt}
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    for attempt in range(1, 4):
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    GEMINI_URL,
                    json=payload,
                    headers=headers
                )
                resp.raise_for_status()
                data = resp.json()
                
                # Extract text from Gemini response
                raw = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                
                # Try to parse JSON (strip markdown if present)
                if "```" in raw:
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                    raw = raw.split("```")[0]
                
                usernames: list[str] = json.loads(raw)
                
                # Sanitize
                clean = [
                    u.lower().strip()
                    for u in usernames
                    if isinstance(u, str) and 3 <= len(u.strip()) <= 30
                ]
                
                await log("INFO", f"Generated {len(clean)} usernames from Gemini API")
                return clean[:30]
                
        except Exception as e:
            await log("WARN", f"Generator attempt {attempt} failed: {e}")
            await asyncio.sleep(3 * attempt)

    await log("ERROR", "All generator attempts failed; returning empty list")
    return []

