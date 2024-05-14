from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.enums.message_answers import AnswerTypes, MessageAnswers
from bot.handlers.commands import cmd_donate
from bot.keyboards.establishment_keyboard import (
    EstablishmentCallback,
    establishments_keyboard,
)
from bot.keyboards.rating_keyboard import RatingCallback, rating_keyboard
from bot.services.api_client import ApiClient
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
    api_client.vote(
        establishment_id=callback_data.establishment_id, vote=callback_data.vote
    )
    text = f"Ви проголосували {callback_data.vote} за {callback_data.establishment_id}, записав!"

    await query.message.answer(text=text)
    await query.answer(text="Ваш голос враховано :)")


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
