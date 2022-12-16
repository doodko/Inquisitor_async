import asyncio

from ping_app.ping_service import PingService



if __name__ == '__main__':
    service = PingService()
    asyncio.run(service.fake_ping())
