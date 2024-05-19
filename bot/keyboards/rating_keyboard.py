from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.types.search_dto import Establishment


class RatingCallback(CallbackData, prefix="rating"):
    establishment_id: int
    establishment_name: str
    vote: int
    emoji: str


class ShareCallback(CallbackData, prefix="share"):
    establishment_id: int
    slug: str


def rating_keyboard(establishment: Establishment):
    emoji_ratings = {"💩": 1, "👎": 2, "😐": 3, "👍": 4, "😍": 5}
    trimmed_establishment_name = (
        establishment.name[:10] if len(establishment.name) > 10 else establishment.name
    )

    builder = InlineKeyboardBuilder()
    for emoji, vote in emoji_ratings.items():
        callback_data = RatingCallback(
            establishment_id=establishment.id,
            establishment_name=trimmed_establishment_name,
            vote=vote,
            emoji=emoji,
        )
        builder.button(text=emoji, callback_data=callback_data)

    builder.adjust(5)

    return builder.as_markup()
