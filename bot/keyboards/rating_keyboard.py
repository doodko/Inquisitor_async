from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.types.search_dto import Establishment


class RatingCallback(CallbackData, prefix="rating"):
    establishment_id: int
    vote: int


def rating_keyboard(establishment: Establishment):
    emoji_ratings = {"💩": 1, "👎": 2, "😐": 3, "👍": 4, "😍": 5}

    builder = InlineKeyboardBuilder()
    for emoji, vote in emoji_ratings.items():
        callback_data = RatingCallback(establishment_id=establishment.id, vote=vote)
        builder.button(text=emoji, callback_data=callback_data)

    builder.adjust(5)
    return builder.as_markup()
