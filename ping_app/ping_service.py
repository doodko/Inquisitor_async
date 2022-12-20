import asyncio
import subprocess
import platform
from random import choice

from aiogram import Bot
from loguru import logger

from ping_app.host_service import host_crud_service
from ping_app.models import Zone, Host
from ping_app.notifier_service import NotifierService
from settings_reader import config


bot = Bot(token=config.token.get_secret_value(), parse_mode="HTML")
notifier = NotifierService()


class PingService:
    async def start_service(self):
        await bot.send_message(chat_id=config.superuser_id, text='Service started')
        logger.info('Ping service started')
        while config.ping_flag:
            await self.ping_random_hosts()
            await asyncio.sleep(config.ping_period)

    @staticmethod
    async def ping_host(host: Host) -> bool:
        logger.debug(f"ping {host.name} - {host.address}")
        ip = host.address
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '2', ip]
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

            if host_status != host.zone_group.is_online:
                await self.check_zone_status(zone=host.zone_group)

    async def check_zone_status(self, zone: Zone):
        zone_status = any([await self.ping_host(host=host) for host in zone.addresses])

        if zone_status != zone.is_online:
            await self.zone_status_switched(zone=zone)

    @staticmethod
    async def zone_status_switched(zone: Zone):
        current_zone_message = notifier.get_changed_state(instance=zone)
        logger.info(current_zone_message)
        await host_crud_service.invert_online_status(instance=zone)

        # other_zone = await host_crud_service.get_other_zone(zone=zone)
        # other_zone_message = notifier.get_current_state(instance=other_zone)
        # answer = f"{current_zone_message}\n{other_zone_message}"

        answer = f"{current_zone_message}"

        emodji = ('⚡', '💡')
        destination = '-1001092707720'  # config.superuser_id
        await bot.send_message(chat_id=destination, text=f"{emodji[zone.is_online]}")
        await bot.send_message(chat_id=destination, text=answer)

    @staticmethod
    async def get_current_zones_status() -> str:
        zones = await host_crud_service.get_all_zones()
        zone_statuses = [notifier.get_current_state(zone) for zone in zones]
        return '\n'.join(zone_statuses)

    async def ping_all_hots(self):
        hosts = await host_crud_service.get_all_hosts()
        for host in hosts:
            await self.ping_host(host=host)

    async def fake_ping(self):
        coffeeshop: Host = host_crud_service.session.get(Host, 1)
        alex: Host = host_crud_service.session.get(Host, 5)
        hosts = [coffeeshop, alex]

        while config.ping_flag:
            for host in hosts:
                host_status = await self.ping_host(host=host)

                if host_status != host.zone_group.is_online:
                    await self.zone_status_switched(zone=host.zone_group)

            logger.debug('sleeping 60 sec')
            await asyncio.sleep(config.ping_period)
