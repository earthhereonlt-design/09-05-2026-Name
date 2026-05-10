import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.config import Config
from bot.database import db
from bot.handlers.commands import router, get_runner
from bot.utils.helpers import log


async def main():
    # Validate config before starting
    if not Config.validate():
        sys.exit(1)

    # Init DB
    await db.init_db()

    chat_id = int(Config.TELEGRAM_CHAT_ID)
    bot = Bot(
        token=Config.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await log("INFO", "Bot starting up")

    # Auto-resume if was running before restart
    was_running = await db.get_state("running", "0")
    if was_running == "1":
        await log("INFO", "Auto-resuming from previous session")
        runner = get_runner(bot, chat_id)
        asyncio.create_task(runner.start())
        try:
            await bot.send_message(chat_id, "♻️ Auto-resumed after restart.")
        except Exception:
            pass

    await dp.start_polling(bot, allowed_updates=["message"])


if __name__ == "__main__":
    asyncio.run(main())
