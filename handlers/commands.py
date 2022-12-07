from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot import bot
from settings_reader import config


router = Router()
router.message.filter(F.from_user.id.in_(config.admins))


@router.message(Command(commands=['send_message']))
async def cmd_send_message(message: Message):
    msg = message.text[13:]
    await bot.send_message(chat_id='-740613554', text=msg)


@router.message(Command(commands=['health_check']))
async def cmd_health_check(message: Message):
    await message.answer(text="I'm okay!")
