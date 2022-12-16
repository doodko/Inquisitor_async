import asyncio

from loguru import logger

from ping_app.ping_service import PingService


async def main():
    logger.debug('service ping')
    service = PingService()
    await service.fake_ping()


if __name__ == '__main__':
    asyncio.run(main())
