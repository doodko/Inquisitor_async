from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from bot.handlers.commands import cmd_donate

router = Router()
router.message.filter(F.chat.type =='private')


@router.message(F.text.lower().regexp(r"(дякую)|(спасиб)"))
async def text_donate(message: Message):
    await cmd_donate(message)


@router.message()
async def all_other_private_messages(message: Message):
    text = f"other messages | {message.from_user.full_name} | {message.text}"
    logger.bind(private=True).info(text)
    text = '''
На даний момент бот знаходиться в стадії бета тестування. Якщо помітили помилку - напишіть @doodko
'''

    await message.answer(text=text)

