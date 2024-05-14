from aiogram import F, Router
from aiogram.types import Message

from bot.enums.message_answers import AnswerTypes, MessageAnswers

router = Router()
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


regexp_base = r".*((дайте)|.*(ка[жз])|(пиш)|(какой)|(який)).*"
ohorona = regexp_base + r"((телефон)|(номер)).*(ох[о]?р[оа]н[иы])"
service_company = (
    regexp_base + r"((телефон)|(номер)).*((ж[єкеэ][хк])|(комфорт.серв[иі]с))"
)
post_index = regexp_base + r"([іи]ндекс)"


@router.message(F.text.lower().regexp(ohorona))
async def say_security_service_phone(message: Message):
    await message.reply("+380674092276")


@router.message(F.text.lower().regexp(service_company))
async def say_service_company_phone(message: Message):
    await message.reply("+380672247713\n+380670000012 (цілодобовий)")


@router.message(F.text.lower().regexp(post_index))
async def say_index(message: Message):
    await message.reply(text=MessageAnswers.answer(AnswerTypes.POST_INDEX))
