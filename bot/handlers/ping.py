import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import subprocess

from loguru import logger

from settings_reader import config

router = Router()


async def some_func():
    logger.info('some func')


@router.message(Command(commands=['ping']))
async def cmd_ping(message: Message):
    config.ping_flag = not config.ping_flag
    answer = f'flag set to {config.ping_flag}'
    logger.info(answer)
    await message.answer(answer)
    while config.ping_flag:
        task = asyncio.create_task(some_func())
        await asyncio.sleep(5)
        await task

