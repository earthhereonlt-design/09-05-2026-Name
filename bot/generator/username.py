import json
import asyncio
import httpx
import random
from bot.database import db
from bot.utils.helpers import log
from bot.config import Config

# Configuration
GEMINI_API_KEY = Config.GEMINI_API_KEY
# Using the v1beta endpoint with API key in the URL for better compatibility
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Pattern variations for local fallback and prompt context
DOT_SUFFIXES = [
    "ai", "ml", "vr", "xr", "db", "ui", "ux", "os", "gg", "ff", 
    "tt", "dev", "it", "cc", "tv", "rx", "tx", "dx", "cx", "pk", 
    "kz", "jp", "kr", "uk", "us", "in", "qa", "id", "am", "io",
    "co", "me", "app", "web"
]

UNDERSCORE_SUFFIXES = [
    "ai", "ml", "vr", "xr", "db", "ui", "ux", "os", "rx", "tx",
    "dx", "cx", "pk", "jp", "kr", "uk", "us", "in", "id", "am",
    "bot", "dev", "app", "pro", "lab"
]

BASES = ["aadi", "adi", "aa", "ad"]

SYSTEM_PROMPT = (
    "You are a specialized Instagram username generator. "
    "Generate usernames using these exact patterns:\n"
    "1. base (aadi, adi, aa, ad) + '.' + suffix (e.g., aadi.ai)\n"
    "2. base + '_' + suffix (e.g., adi_dev)\n"
    "3. base + 2-letter country codes (e.g., aa.in)\n"
    "Return ONLY a JSON array of strings. No conversational text or markdown blocks."
)

def generate_local_fallback(used: set[str], count: int = 30) -> list[str]:
    """
    Generates usernames algorithmically if the API fails or is rate-limited.
    Ensures the bot remains functional without external dependencies.
    """
    pool = []
    for b in BASES:
        for s in DOT_SUFFIXES:
            pool.append(f"{b}.{s}")
        for s in UNDERSCORE_SUFFIXES:
            pool.append(f"{b}_{s}")
        # Add common country code variations
        for cc in ["in", "us", "uk", "jp", "kr"]:
            pool.append(f"{b}.{cc}")
            pool.append(f"{b}_{cc}")
    
    # Filter out names that have already been checked/used
    available = [u for u in pool if u not in used]
    random.shuffle(available)
    return available[:count]

async def generate_usernames(used: set[str]) -> list[str]:
    """
    Call Gemini API with JSON mode and exponential backoff.
    Falls back to local generation if API is exhausted or returns 429.
    """
    # Sample the last 50 names to avoid bloat in the prompt
    used_sample = list(used)[-50:] if len(used) > 50 else list(used)
    
    user_prompt = (
        f"Generate 30 unique usernames following the system rules. "
        f"Skip these recently seen names: {', '.join(used_sample) if used_sample else 'none'}. "
        "Format: ['user1', 'user2', ...]"
    )

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "response_mime_type": "application/json",
            "temperature": 0.85
        }
    }

    headers = {"Content-Type": "application/json"}

    for attempt in range(1, 6):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(GEMINI_URL, json=payload, headers=headers)
                
                # Specific handling for Rate Limits
                if response.status_code == 429:
                    wait = (2 ** attempt) + random.uniform(0.1, 1.0) # Exponential backoff + jitter
                    await log("WARN", f"Rate Limited (429). Attempt {attempt}/5. Retrying in {wait:.1f}s")
                    await asyncio.sleep(wait)
                    continue

                response.raise_for_status()
                result = response.json()
                
                try:
                    # Extract text content from the Gemini response structure
                    raw_text = result['candidates'][0]['content']['parts'][0]['text']
                    usernames = json.loads(raw_text)
                    
                    if not isinstance(usernames, list):
                        raise ValueError("API response was not a JSON list")

                    # Sanitize and validate lengths
                    clean = [
                        u.lower().strip() for u in usernames 
                        if isinstance(u, str) and 3 <= len(u.strip()) <= 30
                    ]
                    
                    if clean:
                        await log("INFO", f"Successfully generated {len(clean)} names via Gemini.")
                        return clean[:30]
                        
                except (KeyError, IndexError, ValueError, json.JSONDecodeError) as e:
                    await log("ERROR", f"Failed to parse API response on attempt {attempt}: {e}")
                    
        except httpx.HTTPError as e:
            await log("WARN", f"Network error on attempt {attempt}: {e}")
            await asyncio.sleep(1.5 * attempt)
        except Exception as e:
            await log("ERROR", f"Critical error on attempt {attempt}: {e}")
            await asyncio.sleep(1.5 * attempt)

    # Final Fallback: If the loop finishes without returning, the API is unavailable
    await log("INFO", "Gemini API unavailable after 5 retries. Falling back to local generation.")
    return generate_local_fallback(used, 30)
