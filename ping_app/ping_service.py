import asyncio
import subprocess
import platform
from random import choice

from aiogram import Bot
from loguru import logger
from aiogram.exceptions import TelegramForbiddenError

from ping_app.host_service import host_crud_service
from ping_app.models import Zone, Host
from ping_app.notifier_service import NotifierService
from ping_app.periods_service import PeriodService
from settings_reader import config


bot = Bot(token=config.token.get_secret_value(), parse_mode="HTML")
notifier = NotifierService()
period_service = PeriodService()


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
                await self.check_other_hosts(switched_host=host)

    async def check_zone_status(self, zone: Zone):
        zone_status = False
        for host in zone.addresses:
            is_online = await self.ping_host(host=host)
            if is_online:
                zone_status = True
                break

        if zone_status != zone.is_online:
            await self.zone_status_switched(zone=zone)

    async def check_other_hosts(self, switched_host: Host):
        zone_status = False
        zone = switched_host.zone_group
        other_hosts = await host_crud_service.get_other_hosts_in_zone(host=switched_host)

        for host in other_hosts:
            is_online = await self.ping_host(host=host)
            if is_online:
                zone_status = True
                break

        if zone_status != zone.is_online:
            await self.zone_status_switched(zone=zone)

    async def zone_status_switched(self, zone: Zone):
        online_message = ('up', 'down')
        text = f"{zone.name} is {online_message[zone.is_online]} now!"
        logger.bind(zone=True).info(text)

        current_zone_message = notifier.get_changed_state(instance=zone)
        await host_crud_service.invert_online_status(instance=zone)
        await period_service.start_stop_period(zone=zone)
        group_msg = current_zone_message + self._finish_message(zone.is_online)
        await self.notify_main_group(zone=zone, message=group_msg)
        await self.notify_subscribers(zone=zone, message=current_zone_message)

    @staticmethod
    async def notify_main_group(zone: Zone, message: str):
        destination = '-1001092707720'  # config.superuser_id
        emodji = ('⚡', '💡')
        await bot.send_message(chat_id=destination, text=f"{emodji[zone.is_online]}")
        await bot.send_message(chat_id=destination, text=message)

    @staticmethod
    def _finish_message(is_online: bool) -> str:
        light_on = choice(['Стало трохи краще', 'Ну нарешті!', 'Привіт, ми чекали', 'Ура!', 'Електрохарчування подано',
                           'Більше не змушуй мене так довго чекати!', 'Майже вчасно', 'Не пройшло і пів дня',
                           'Непогано', 'Слава нації, кінець російській федерації', 'Свєта, давай частіше зустрічатись'])

        light_off = choice(['Йбн рсня!', 'А шо так мало?', 'Наша русофобія недостатня.', 'Свєта, вєртайся.',
                            'Було добре, можна добавки', 'Ну ще 5 хвилин...', 'Стало гірше :(', 'Я хочу ще',
                            'Нема сечі терпіти ці пекельні борошна', 'І це й все?.. а розмов то було',
                            'І на тому спасибі'])

        msg_finish = (light_off, light_on)
        return '\n\n' + msg_finish[is_online]

    @staticmethod
    async def notify_subscribers(zone: Zone, message: str):
        for subscription in zone.subscribers:
            try:
                await bot.send_message(chat_id=subscription.user_id, text=message)
            except TelegramForbiddenError:
                logger.info(f"user {subscription.user_id} blocked the bot")
                host_crud_service.session.delete(subscription)
                host_crud_service.session.commit()

    async def ping_all_hots(self):
        hosts = await host_crud_service.get_all_hosts()
        for host in hosts:
            await self.ping_host(host=host)

    @staticmethod
    async def get_current_zones_status() -> str:
        zones = await host_crud_service.get_all_zones()
        zone_statuses = [notifier.get_current_state(zone) for zone in zones]
        return '\n\n'.join(zone_statuses)

    @staticmethod
    async def change_ping_periodicity(seconds: str) -> str:
        message = f"invalid value"
        if seconds.isnumeric():
            if int(seconds) != config.ping_period:
                config.ping_period = int(seconds)
                message = f"ping period was changed to {seconds} seconds"
                logger.bind(event=True).info(message)

        return message
