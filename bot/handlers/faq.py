from aiogram import F, Router
from aiogram.types import Message

from bot.services.mixpanel_client import mp
from bot.types.enums import MixpanelEvents

router = Router()
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


regexp_base = r".*((дайте)|.*(ка[жз])|(пиш)|(какой)|(який)).*"
ohorona = regexp_base + r"((телефон)|(номер)).*(ох[о]?р[оа]н[иы])"
service_company = (
    regexp_base + r"((телефон)|(номер)).*((ж[єкеэ][хк])|(комфорт.серв[иі]с))"
)


@router.message(F.text.lower().regexp(ohorona))
async def say_security_service_phone(message: Message):
    await message.reply("+380674092276")
    mp.track_event(
        user=message.from_user,
        event=MixpanelEvents.HINT,
        event_properties={"type": "security", "message": message.text},
    )


@router.message(F.text.lower().regexp(service_company))
async def say_service_company_phone(message: Message):
    await message.reply("+380672247713\n+380670000012 (цілодобовий)")
    mp.track_event(
        user=message.from_user,
        event=MixpanelEvents.HINT,
        event_properties={"type": "service_company", "message": message.text},
    )
