import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from bot.handlers import commands, faq, private_messages
from bot.services.sentry_setup import sentry_init
from bot.settings_reader import config

bot = Bot(
    token=config.token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>",
)
logger.add(
    "logs/{time:YYYY-MM-DD}/event.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
    filter=lambda record: "event" in record["extra"],
    rotation="1 day",
)


async def main():
    sentry_init()

    dp = Dispatcher()

    dp.include_router(commands.router)
    dp.include_router(faq.router)
    dp.include_router(private_messages.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await send_message(text="Bot started")
    await dp.start_polling(bot)


async def send_message(chat_id: int = config.superuser_id, text: str = "some_text"):
    await bot.send_message(chat_id=chat_id, text=text)


if __name__ == "__main__":
    asyncio.run(main())
