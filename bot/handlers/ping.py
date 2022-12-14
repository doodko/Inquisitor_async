from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from ping_app.host_service import host_crud_service
from ping_app.ping_service import PingService
from settings_reader import config


router = Router()
router.message.filter(F.from_user.id.in_(config.admins))

ps = PingService()


@router.message(Command(commands=['ping']))
async def cmd_start_ping(message: Message):
    config.ping_flag = not config.ping_flag
    await message.answer(text=f'Ping service switched to {config.ping_flag}')


@router.message(Command(commands=['update_zone_time']))
async def cmd_update_time(message: Message):
    command, zone_id, new_time = message.text.split()
    text = await host_crud_service.update_zone_time(zone_id=zone_id, new_time=new_time)
    await message.answer(text=text)


@router.message(Command(commands=['ping_period']))
async def cmd_ping_period(message: Message):
    lst = message.text.split()
    if len(lst) == 1:
        await message.answer(f"ping period is {config.ping_period} seconds now")
    elif len(lst) == 2:
        command, new_period = lst
        answer = await ps.change_ping_periodicity(new_period)
        await message.answer(answer)
