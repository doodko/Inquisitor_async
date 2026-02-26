from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, User
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.settings_reader import config
from bot.types.search_dto import Establishment


class RatingCallback(CallbackData, prefix="rating"):
    obj_id: int
    obj_name: str
    vote: int
    emoji: str


class ShareCallback(CallbackData, prefix="share"):
    obj_id: int
    slug: str


class LocationCallback(CallbackData, prefix="location"):
    coords: str


def rating_keyboard(establishment: Establishment, user: User) -> InlineKeyboardMarkup:
    emoji_ratings = {"💩": 1, "👎": 2, "😐": 3, "👍": 4, "😍": 5}
    trimmed_establishment_name = (
        establishment.name[:10] if len(establishment.name) > 10 else establishment.name
    )

    builder = InlineKeyboardBuilder()
    for emoji, vote in emoji_ratings.items():
        callback_data = RatingCallback(
            obj_id=establishment.id,
            obj_name=trimmed_establishment_name,
            vote=vote,
            emoji=emoji,
        )
        builder.button(text=emoji, callback_data=callback_data)
        builder.adjust(5)

    if establishment.address and establishment.address.location:
        callback_data = LocationCallback(coords=establishment.address.location).pack()
        map_button = InlineKeyboardButton(
            text="Показати на мапі 🗺️", callback_data=callback_data
        )
        builder.row(map_button)

    if user.id in config.admins:
        callback_data = ShareCallback(
            obj_id=establishment.id, slug=establishment.slug
        ).pack()
        extra_button = InlineKeyboardButton(text="Share", callback_data=callback_data)
        builder.row(extra_button)

    return builder.as_markup()
