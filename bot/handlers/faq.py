from random import choice

from aiogram import Router, F
from aiogram.types import Message

from ping_app.ping_service import PingService

router = Router()
ps = PingService()


regexp_base = r".*((дайте)|.*(ка[жз])|(пиш)|(какой)|(який)).*"
ohorona = regexp_base + r"((телефон)|(номер)).*(ох[о]?р[оа]н[иы])"
service_company = regexp_base + r"((телефон)|(номер)).*((ж[єкеэ][хк])|(комфорт.серв[иі]с))"
post_index = regexp_base + r"([іи]ндекс)"


@router.message(F.text.lower().regexp(ohorona))
async def say_security_service_phone(message: Message):
    await message.reply("+380674092276")


@router.message(F.text.lower().regexp(service_company))
async def say_service_company_phone(message: Message):
    await message.reply("+380672247713\n+380670000012 (цілодобовий)")


@router.message(F.text.lower().regexp(post_index))
async def say_index(message: Message):
    await message.reply("індекс: 08148")


@router.message(F.text.lower().regexp(r".*(\bсвітло\b.*\bє\b).*|.*(\bє\b.*\bсвітло\b).*\?"))
async def say_current_status(message: Message):
    text = await ps.get_current_zones_status()
    await message.reply(text=text)


@router.message(F.text.lower().regexp(r".*(\bсвет\b.*\bесть\b).*|.*(\bесть\b.*\bсвет\b).*\?"))
async def say_current_status(message: Message):
    answers = ("Я знаю, проте не скажу! 🤓", "🤪 расєянську не разумєю", "Запитай мене солов'їною 😍")
    await message.reply(text=choice(answers))
