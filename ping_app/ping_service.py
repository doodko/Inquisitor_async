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
            logger.info("-----------------------------------------------")
            await asyncio.sleep(config.ping_period)

    @staticmethod
    async def ping_host(host: Host) -> bool:
        ip = host.address
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '2', ip]
        is_online = subprocess.run(args=command, stdout=subprocess.DEVNULL).returncode == 0

        if host.is_online != is_online:
            await host_crud_service.invert_online_status(instance=host)

        online_message = ('down', 'up')
        logger.info(f"ping {host.address} (group {host.zone}) - it's {online_message[is_online]}!")
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
        logger.debug(current_zone_message)
        await host_crud_service.invert_online_status(instance=zone)

        online_message = ('down', 'up')
        text = f"{zone.name} is {online_message[zone.is_online]} now!"
        logger.bind(zone=True).info(text)

        answer = f"{current_zone_message}"

        emodji = ('⚡', '💡')
        destination = '-1001092707720' # config.superuser_id
        await bot.send_message(chat_id=destination, text=f"{emodji[zone.is_online]}")
        await bot.send_message(chat_id=destination, text=answer)

    @staticmethod
    async def get_current_zones_status() -> str:
        zones = await host_crud_service.get_all_zones()
        zone_statuses = [notifier.get_current_state(zone) for zone in zones]
        return '\n'.join(zone_statuses)

    @staticmethod
    async def get_current_zones_status_short() -> str:
        zones = await host_crud_service.get_all_zones()
        zone_statuses = [notifier.get_current_state_short(zone) for zone in zones]
        return '\n'.join(zone_statuses)

    async def ping_all_hots(self):
        hosts = await host_crud_service.get_all_hosts()
        for host in hosts:
            await self.ping_host(host=host)

