import time
import asyncio
from pathlib import Path
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from bot.config import Config
from bot.services.runner import BotRunner
from bot.database import db
from bot.utils.helpers import format_duration, log

router   = Router()
_runner: BotRunner | None = None
CHAT_ID = int(Config.TELEGRAM_CHAT_ID)


def get_runner(bot: Bot, chat_id: int) -> BotRunner:
    global _runner
    if _runner is None:
        _runner = BotRunner(bot, chat_id)
    return _runner


def _guard(message: Message) -> bool:
    """Only respond to the configured chat."""
    return message.chat.id == CHAT_ID


@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
    if not _guard(message):
        return
    await message.answer(
        "🤖 *Instagram Username Bot*\n\n"
        "Available commands:\n"
        "/run - Start the username finder\n"
        "/stop - Stop the finder\n"
        "/status - Check bot status\n"
        "/log - View recent logs\n"
        "/export - Export available usernames",
        parse_mode="Markdown"
    )


@router.message(Command("run"))
async def cmd_run(message: Message, bot: Bot):
    if not _guard(message):
        return
    runner = get_runner(bot, CHAT_ID)
    if runner.is_running:
        await message.answer("⚡ Already running.")
        return
    await message.answer("🚀 Starting username finder loop...")
    await runner.start()


@router.message(Command("stop"))
async def cmd_stop(message: Message, bot: Bot):
    if not _guard(message):
        return
    runner = get_runner(bot, CHAT_ID)
    if not runner.is_running:
        await message.answer("💤 Not running.")
        return
    await message.answer("🛑 Stopping...")
    await runner.stop()
    await message.answer("✅ Stopped.")


@router.message(Command("status"))
async def cmd_status(message: Message, bot: Bot):
    if not _guard(message):
        return
    runner  = get_runner(bot, CHAT_ID)
    checked = await db.get_stat("total_checked")
    avail   = await db.get_stat("total_available")
    errors  = await db.get_stat("total_errors")
    rl      = await db.get_stat("total_rate_limits")
    cur     = await db.get_stat("current_username")
    start_ts = await db.get_stat("start_time")
    runtime = format_duration(time.time() - float(start_ts)) if start_ts else "—"
    state   = "🟢 Running" if runner.is_running else "🔴 Stopped"

    text = (
        f"*Bot Status*\n\n"
        f"Status: {state}\n"
        f"🔍 Checking: `{cur or '—'}`\n"
        f"✅ Total checked: `{checked}`\n"
        f"🟢 Available found: `{avail}`\n"
        f"❌ Errors: `{errors}`\n"
        f"⏳ Rate limits: `{rl}`\n"
        f"🕐 Runtime: `{runtime}`"
    )
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("log"))
async def cmd_log(message: Message, bot: Bot):
    if not _guard(message):
        return
    logs = await db.get_last_logs(5)
    if not logs:
        await message.answer("📭 No logs yet.")
        return
    lines = []
    for entry in logs:
        ts = entry["at"].split("T")[-1][:8]
        lines.append(f"`[{ts}]` [{entry['level']}] {entry['msg']}")
    await message.answer("\n".join(lines), parse_mode="Markdown")


@router.message(Command("export"))
async def cmd_export(message: Message, bot: Bot):
    if not _guard(message):
        return
    usernames = await db.get_all_available()
    if not usernames:
        await message.answer("📭 No available usernames found yet.")
        return
    out = Path("data/available.txt")
    out.write_text("\n".join(usernames))
    await bot.send_document(
        CHAT_ID,
        FSInputFile(out, filename="available_usernames.txt"),
        caption=f"📦 {len(usernames)} available username(s)",
    )


@router.message(Command("clear"))
async def cmd_clear(message: Message, bot: Bot):
    if not _guard(message):
        return
    await db.clear_all()
    await log("INFO", "Stats and logs cleared by user")
    await message.answer("🗑️ Logs and stats cleared.")


@router.message(Command("help"))
async def cmd_help(message: Message, bot: Bot):
    if not _guard(message):
        return
    text = (
        "*Available Commands*\n\n"
        "/run — Start the finder loop\n"
        "/stop — Gracefully stop\n"
        "/status — Show live stats\n"
        "/log — Show last 5 logs\n"
        "/export — Export available usernames as .txt\n"
        "/clear — Clear logs and stats\n"
        "/help — This message"
    )
    await message.answer(text, parse_mode="Markdown")
