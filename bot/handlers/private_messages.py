import random

from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

router = Router()
router.message.filter(F.chat.type =='private')


@router.message()
async def all_other_private_messages(message: Message):
    text = f"{message.from_user.id} | {message.from_user.full_name} say: {message.text}"
    logger.bind(private=True).info(text)
    answers = ("Я не знаю що ви від мене хочте 🤷‍♂",
               "Скоро я навчусь повідомляти коли з'являється чи зникає світло в ПК прямо Вам "
               "в приватні повідомлення, а поки що запитайте мене, якщо вам це цікаво.",
               "Запитай чи є світло або не мороч мені голову!")

    await message.answer(text=random.choice(answers))
