from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.enums.message_answers import AnswerTypes, MessageAnswers
from bot.handlers.commands import cmd_donate
from bot.keyboards.establishment_keyboard import (
    EstablishmentCallback,
    establishments_keyboard,
)
from bot.services.api_client import api_client
from bot.services.establishment_reply_builder import EstablishmentBuilder
from bot.services.private_message_service import private_message_service
from bot.types.search_dto import SearchResponse

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(F.text.lower().regexp(r"(дякую)|(спасиб)"))
async def text_donate(message: Message):
    await cmd_donate(message)


@router.callback_query(EstablishmentCallback.filter())
async def process_establishment(
    query: CallbackQuery, callback_data: EstablishmentCallback
):

    establishment = api_client.retrieve(slug=callback_data.slug)
    if not establishment:
        answer = MessageAnswers.answer(AnswerTypes.ERROR_MESSAGE)
    else:
        answer = EstablishmentBuilder(establishment).build_establishment_card()

    await query.message.answer(text=answer)
    await query.answer()


@router.message(F.text)
async def all_other_private_messages(message: Message):
    answer = await private_message_service.process_private_message(message=message)

    if isinstance(answer, str):
        await message.answer(answer)
    elif isinstance(answer, SearchResponse):
        await message.answer(
            text=MessageAnswers.answer(AnswerTypes.SUCCESSFUL_SEARCH),
            reply_markup=establishments_keyboard(establishments=answer.result),
        )
    else:
        await message.answer(text=MessageAnswers.answer(AnswerTypes.ERROR_MESSAGE))
