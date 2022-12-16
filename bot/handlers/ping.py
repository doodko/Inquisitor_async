from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import subprocess


router = Router()


@router.message(Command(commands=['ping']))
async def cmd_ping(message: Message):
    host = message.text.split()[1]
    command = ['ping', '-n', '1', host]
    if subprocess.call(command) == 0:
        answer = host + " is up!"
    else:
        answer = host + " is down!"

    await message.answer(answer)
