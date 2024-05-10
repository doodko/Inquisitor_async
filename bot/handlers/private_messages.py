from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from bot.handlers.commands import cmd_donate
from bot.services.search_service import search_service
from bot.types.search_dto import SearchResponse

router = Router()
router.message.filter(F.chat.type =='private')


@router.message(F.text.lower().regexp(r"(дякую)|(спасиб)"))
async def text_donate(message: Message):
    await cmd_donate(message)


@router.message()
async def all_other_private_messages(message: Message):
    log_text = f"other messages | {message.from_user.full_name} | {message.text}"
    logger.bind(private=True).info(log_text)

    if len(message.text) < 3:
        answer_text = "Your search query should contain at least 3 symbols."
    elif len(message.text.split()) > 3:
        answer_text = "Your search query should contain no more than 3 words."
    else:
        search_response = search_service.find(message.text)

        if not search_response:
            answer_text = "Сталась якась халепа, спробуйте пізніше :("

        elif search_response.count == 0:
            answer_text = "Мені не вдалось нічого знайти :("

        else:
            answer_text = f"Знайдено {search_response.count} результатів"

    await message.answer(text=answer_text)

