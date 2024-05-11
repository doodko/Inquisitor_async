from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from bot.handlers.commands import cmd_donate
from bot.services.private_message_service import private_message_service
from bot.services.search_service import search_service

router = Router()
router.message.filter(F.chat.type =='private')


@router.message(F.text.lower().regexp(r"(дякую)|(спасиб)"))
async def text_donate(message: Message):
    await cmd_donate(message)


@router.message()
async def all_other_private_messages(message: Message):
    answer = await private_message_service.process_private_message(message=message)
    await message.answer(text=answer)

