import asyncio

from loguru import logger
from aiogram import Bot, Dispatcher

from bot.handlers import faq, commands, ping
from settings_reader import config


bot = Bot(token=config.token.get_secret_value(), parse_mode="HTML")


async def main():
    dp = Dispatcher()

    dp.include_router(commands.router)
    dp.include_router(faq.router)
    dp.include_router(ping.router)

    logger.info('Bot started')

    await bot.delete_webhook(drop_pending_updates=True)
    await send_message(text='Bot started')
    await dp.start_polling(bot)


async def send_message(chat_id: int = config.superuser_id, text: str = 'some_text'):
    await bot.send_message(chat_id=chat_id, text=text)


if __name__ == "__main__":
    asyncio.run(main())
