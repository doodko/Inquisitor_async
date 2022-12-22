import asyncio
import sys

from loguru import logger

from ping_app.ping_service import PingService


logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>")
logger.add("logs/{time:YYYY-MM-DD}_ping.log", format="{time:YYYY-MM-DD HH:mm:ss} | {message}", level='INFO')
# logger.add('logs/info.log', format="{time:YYYY-MM-DD HH:mm:ss} | {message}", level='INFO')



async def main():
    service = PingService()
    await service.start_service()


if __name__ == '__main__':
    asyncio.run(main())
