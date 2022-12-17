from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from ping_app.ping_service import PingService
from settings_reader import config


router = Router()
ps = PingService()


@router.message(Command(commands=['ping']))
async def cmd_start_ping(message: Message):
    config.ping_flag = not config.ping_flag
    await message.answer(text=f'Ping service switched to {config.ping_flag}')


@router.message(Command(commands=['current_status']))
async def cmd_current_status(message: Message):
    await message.delete()
    text = await ps.get_current_zones_status()
    await message.answer(text=text)


@router.message(F.text.lower().regexp(r".*(є|есть|дали).*(світло|свет).*(\?)"))
async def say_current_status(message: Message):
    text = await ps.get_current_zones_status()
    await message.answer(text=text)