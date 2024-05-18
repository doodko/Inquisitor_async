from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.settings_reader import config
from bot.types.search_dto import Establishment


class RatingCallback(CallbackData, prefix="rating"):
    establishment_id: int
    vote: int
    emoji: str


class ShareCallback(CallbackData, prefix="share"):
    establishment_id: int
    slug: str


def rating_keyboard(establishment: Establishment, chat_id: int):
    emoji_ratings = {"💩": 1, "👎": 2, "😐": 3, "👍": 4, "😍": 5}

    builder = InlineKeyboardBuilder()
    for emoji, vote in emoji_ratings.items():
        callback_data = RatingCallback(
            establishment_id=establishment.id, vote=vote, emoji=emoji
        )
        builder.button(text=emoji, callback_data=callback_data)

    builder.adjust(5)

    if chat_id == config.superuser_id:
        callback_data = ShareCallback(
            establishment_id=establishment.id, slug=establishment.slug
        ).pack()
        extra_button = InlineKeyboardButton(text="Share", callback_data=callback_data)
        builder.add(extra_button)
        builder.adjust(5, 1)

    return builder.as_markup()
