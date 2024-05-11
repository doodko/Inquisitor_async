from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.types.search_dto import Establishment


class EstablishmentCallback(CallbackData, prefix='establishment'):
    id: int
    slug: str


def establishments_keyboard(establishments: List[Establishment]):
    builder = InlineKeyboardBuilder()
    for establishment in establishments:
        callback_data = EstablishmentCallback(id=establishment.id, slug=establishment.slug)
        builder.button(text=establishment.name, callback_data=callback_data)

    builder.adjust(1)
    return builder.as_markup()
