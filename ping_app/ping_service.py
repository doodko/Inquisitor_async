import asyncio
import subprocess
from random import choice

from loguru import logger

from bot.start_bot import send_message
from ping_app.host_service import host_crud_service
from ping_app.models import Zone, Host
from ping_app.notifier_service import NotifierService
from settings_reader import config


notifier = NotifierService()


class PingService:
    async def start_service(self):
        logger.info('Start ping service')
        while True:
            await self.ping_random_hosts()
            logger.debug(f'sleeping {config.ping_period} seconds')
            await asyncio.sleep(config.ping_period)

    @staticmethod
    async def ping_host(host: Host) -> bool:
        logger.debug(f"ping {host.name} - {host.address}")
        ip = host.address
        command = ['ping', '-n', '2', ip]
        is_online = subprocess.run(args=command, stdout=subprocess.DEVNULL).returncode == 0

        message = notifier.get_current_state(instance=host)

        if host.is_online != is_online:
            message = notifier.get_changed_state(instance=host)
            await host_crud_service.invert_online_status(instance=host)

        logger.debug(message)
        return is_online

    @staticmethod
    async def get_hosts_for_ping() -> list[Host]:
        zones = await host_crud_service.get_all_zones()
        hosts_list = [choice(zone.addresses) for zone in zones]
        return hosts_list

    async def ping_random_hosts(self):
        for host in await self.get_hosts_for_ping():
            host_status = await self.ping_host(host)

            if host_status != host.is_online:
                await self.check_zone_status(zone=host.zone_group)

    async def check_zone_status(self, zone: Zone) -> str:
        status_lst = [await self.ping_host(host=host) for host in zone.addresses]
        zone_avg = round(sum(status_lst) / len(status_lst))
        zone_status = bool(zone_avg)

        message = notifier.get_current_state(instance=zone)

        if zone_status != zone.is_online:
            message = notifier.get_changed_state(instance=zone)
            await host_crud_service.invert_online_status(instance=zone)

        logger.info(message)
        return message

    async def ping_all_hots(self):
        hosts = await host_crud_service.get_all_hosts()
        for host in hosts:
            await self.ping_host(host=host)

    async def ping_all_async(self):
        hosts = await host_crud_service.get_all_hosts()
        for host in hosts:
            task = asyncio.create_task(self.ping_host(host=host))
            await task

    async def fake_ping(self):
        coffeeshop = host_crud_service.session.get(Host, 1)
        alex = host_crud_service.session.get(Host, 5)
        hosts = [coffeeshop, alex]

        for host in hosts:
            host_status = await self.ping_host(host=host)

            if host_status != host.zone_group.is_online:
                message = notifier.get_changed_state(instance=host.zone_group)
                await host_crud_service.invert_online_status(instance=host.zone_group)

                logger.info(message)
                await send_message(message)
