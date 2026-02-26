from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.handlers.commands import cmd_donate
from bot.keyboards.establishment_keyboard import (
    EstablishmentCallback,
    establishments_keyboard,
)
from bot.keyboards.rating_keyboard import (
    LocationCallback,
    RatingCallback,
    ShareCallback,
    rating_keyboard,
)
from bot.services.api_client import ApiClient
from bot.services.establishment_reply_builder import EstablishmentBuilder
from bot.services.mixpanel_client import mp
from bot.services.private_message_service import private_message_service
from bot.types.enums import AnswerTypes, MixpanelEvents
from bot.types.message_answers import MessageAnswers
from bot.types.search_dto import SearchResponse

router = Router()
router.message.filter(F.chat.type == "private")


light_regexp = r".*\b(світл[о|а]|свет|граф[і|и]к|дт[е|э]к).*"


@router.message(F.text.lower().regexp(r"(дякую)|(спасиб)"))
async def text_donate(message: Message):
    await cmd_donate(message)


@router.message(F.text.lower().regexp(light_regexp))
async def handle_electricity_questions(message: Message):
    answer = MessageAnswers.answer(AnswerTypes.LIGHT)
    await message.reply(text=answer)
    mp.track_event(
        user=message.from_user,
        event=MixpanelEvents.LIGHT,
        event_properties={"message": message.text.lower(), "answer": answer},
    )


@router.callback_query(EstablishmentCallback.filter())
async def process_establishment_retrieve(
    query: CallbackQuery, callback_data: EstablishmentCallback
):
    user = query.from_user
    api_client = ApiClient(user=user)
    establishment = api_client.retrieve(slug=callback_data.slug)
    if establishment:
        answer = EstablishmentBuilder(establishment).build_establishment_card()
        keyboard = rating_keyboard(establishment=establishment, user=user)

        await query.message.answer(text=answer, reply_markup=keyboard)
        mp.track_event(
            user=user,
            event=MixpanelEvents.RETRIEVE,
            event_properties={
                "message": establishment.slug,
                "answer": establishment.name,
            },
        )

    else:
        answer = MessageAnswers.answer(AnswerTypes.ERROR_MESSAGE)
        await query.message.answer(text=answer)
        mp.track_event(
            user=query.from_user,
            event=MixpanelEvents.ERROR,
            event_properties={"message": establishment.name, "answer": answer},
        )

    await query.answer()


@router.callback_query(RatingCallback.filter())
async def process_rating(query: CallbackQuery, callback_data: RatingCallback):
    api_client = ApiClient(user=query.from_user)
    answer = f"{MessageAnswers.answer(AnswerTypes.VOTED)} {callback_data.emoji}"
    await query.message.answer(text=answer)

    api_client.vote(establishment_id=callback_data.obj_id, vote=callback_data.vote)
    await query.answer()
    mp.update_user_properties(user=query.from_user)
    mp.track_event(
        user=query.from_user,
        event=MixpanelEvents.VOTE,
        event_properties={
            "message": f"{callback_data.obj_name} - {callback_data.emoji}",
            "answer": answer,
        },
    )


@router.callback_query(ShareCallback.filter())
async def process_share(query: CallbackQuery, callback_data: ShareCallback):
    answer = f"<code>/share {callback_data.slug}</code>"
    await query.message.answer(text=answer)
    await query.answer()


@router.callback_query(LocationCallback.filter())
async def show_location(query: CallbackQuery, callback_data: LocationCallback):
    latitude, longitude = callback_data.coords.split(",")
    await query.message.answer_location(latitude=latitude, longitude=longitude)
    await query.answer()


@router.message(F.text)
async def all_other_private_messages(message: Message):
    answer = await private_message_service.process_private_message(message=message)

    if isinstance(answer, str):
        await message.answer(answer)
    elif isinstance(answer, SearchResponse):
        if answer.count == 1:
            establishment = answer.result[0]
            user = message.from_user

            answer = EstablishmentBuilder(establishment).build_establishment_card()
            keyboard = rating_keyboard(establishment=establishment, user=user)

            await message.answer(text=answer, reply_markup=keyboard)
            mp.track_event(
                user=user,
                event=MixpanelEvents.RETRIEVE,
                event_properties={
                    "message": establishment.slug,
                    "answer": establishment.name,
                },
            )
        else:
            await message.answer(
                text=MessageAnswers.answer(AnswerTypes.SUCCESSFUL_SEARCH),
                reply_markup=establishments_keyboard(establishments=answer.result),
            )

    else:
        await message.answer(text=MessageAnswers.answer(AnswerTypes.ERROR_MESSAGE))
