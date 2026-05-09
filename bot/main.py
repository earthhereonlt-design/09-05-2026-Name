import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.database import db
from bot.handlers.commands import router, get_runner
from bot.utils.helpers import log

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID        = int(os.getenv("TELEGRAM_CHAT_ID", "0"))


async def main():
    # Init DB
    await db.init_db()

    bot = Bot(
        token=TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await log("INFO", "Bot starting up")

    # Auto-resume if was running before restart
    was_running = await db.get_state("running", "0")
    if was_running == "1":
        await log("INFO", "Auto-resuming from previous session")
        runner = get_runner(bot)
        asyncio.create_task(runner.start())
        try:
            await bot.send_message(CHAT_ID, "♻️ Auto-resumed after restart.")
        except Exception:
            pass

    await dp.start_polling(bot, allowed_updates=["message"])


if __name__ == "__main__":
    asyncio.run(main())
