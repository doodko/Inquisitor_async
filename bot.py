import asyncio
import logging
from aiogram import Bot, Dispatcher

from handlers import commands, faq
from settings_reader import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token.get_secret_value())


async def main():
    dp = Dispatcher()

    dp.include_router(commands.router)
    dp.include_router(faq.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.send_message(chat_id=config.superuser_id, text='Bot started')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
