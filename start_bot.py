import asyncio
import sys

from loguru import logger
from aiogram import Bot, Dispatcher


from bot.handlers import faq, commands, ping, subscription, private_messages
from settings_reader import config


bot = Bot(token=config.token.get_secret_value(), parse_mode="HTML")

logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>")
logger.add("logs/{time:YYYY-MM-DD}/private.log",
           format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
           filter=lambda record: "private" in record["extra"],
           rotation="1 day")
logger.add("logs/{time:YYYY-MM-DD}/events.log",
           format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
           filter=lambda record: "event" in record["extra"],
           rotation="1 day")


async def main():
    dp = Dispatcher()

    dp.include_router(commands.router)
    dp.include_router(faq.router)
    dp.include_router(ping.router)
    dp.include_router(subscription.router)
    dp.include_router(private_messages.router)

    logger.bind(event=True).info('Bot started')

    await bot.delete_webhook(drop_pending_updates=True)
    await send_message(text='Bot started')
    await dp.start_polling(bot)


async def send_message(chat_id: int = config.superuser_id, text: str = 'some_text'):
    await bot.send_message(chat_id=chat_id, text=text)


if __name__ == "__main__":
    asyncio.run(main())
