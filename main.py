import asyncio
import sys

from loguru import logger

from start_bot import main as bot
from pinsg_start import main as ping


logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>")


async def main():
    task1 = asyncio.create_task(bot())
    task2 = asyncio.create_task(ping())

    await task1
    await task2


if __name__ == '__main__':
    asyncio.run(main())