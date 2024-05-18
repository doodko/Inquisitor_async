from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from loguru import logger

from bot.handlers.commands import cmd_donate
from bot.keyboards.establishment_keyboard import (
    EstablishmentCallback,
    establishments_keyboard,
)
from bot.keyboards.rating_keyboard import RatingCallback, rating_keyboard
from bot.services.api_client import ApiClient
from bot.services.establishment_reply_builder import EstablishmentBuilder
from bot.services.private_message_service import private_message_service
from bot.types.enums import AnswerTypes
from bot.types.message_answers import MessageAnswers
from bot.types.search_dto import SearchResponse

router = Router()
router.message.filter(F.chat.type == "private")


light_regexp = r".*\b(світло|свет|генератор|графік|график|дтек)\b.*"


@router.message(F.text.lower().regexp(r"(дякую)|(спасиб)"))
async def text_donate(message: Message):
    await cmd_donate(message)


@router.message(F.text.lower().regexp(light_regexp))
async def handle_special_words(message: Message):
    log_text = f"electricity questions | {message.from_user.full_name} | {message.text}"
    logger.bind(private=True).info(log_text)
    answer = MessageAnswers.answer(AnswerTypes.LIGHT)
    await message.reply(text=answer)


@router.callback_query(EstablishmentCallback.filter())
async def process_establishment(
    query: CallbackQuery, callback_data: EstablishmentCallback
):
    api_client = ApiClient(user=query.from_user)
    establishment = api_client.retrieve(slug=callback_data.slug)
    if establishment:
        answer = EstablishmentBuilder(establishment).build_establishment_card()
        keyboard = rating_keyboard(establishment=establishment)
        await query.message.answer(text=answer, reply_markup=keyboard)

    else:
        answer = MessageAnswers.answer(AnswerTypes.ERROR_MESSAGE)
        await query.message.answer(text=answer)

    await query.answer()


@router.callback_query(RatingCallback.filter())
async def process_rating(query: CallbackQuery, callback_data: RatingCallback):
    api_client = ApiClient(user=query.from_user)
    text = f"{MessageAnswers.answer(AnswerTypes.VOTED)} {callback_data.emoji}"
    await query.message.answer(text=text)

    api_client.vote(
        establishment_id=callback_data.establishment_id, vote=callback_data.vote
    )
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
