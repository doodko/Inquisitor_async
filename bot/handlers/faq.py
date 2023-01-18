from random import choice

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from ping_app.ping_service import PingService


router = Router()
ps = PingService()


regexp_base = r".*((дайте)|.*(ка[жз])|(пиш)|(какой)|(який)).*"
ohorona = regexp_base + r"((телефон)|(номер)).*(ох[о]?р[оа]н[иы])"
service_company = regexp_base + r"((телефон)|(номер)).*((ж[єкеэ][хк])|(комфорт.серв[иі]с))"
post_index = regexp_base + r"([іи]ндекс)"
lighting_ukr = r".*((\bсвітло\b.*\bє\b).*|.*(\bє\b.*\bсвітло\b)).*\?"
lighting_ru = r".*((\bсвет\b.*\bесть\b).*|.*(\bесть\b.*\bсвет\b)).*\?"


@router.message(F.text.lower().regexp(ohorona))
async def say_security_service_phone(message: Message):
    await message.reply("+380674092276")


@router.message(F.text.lower().regexp(service_company))
async def say_service_company_phone(message: Message):
    await message.reply("+380672247713\n+380670000012 (цілодобовий)")


@router.message(F.text.lower().regexp(post_index))
async def say_index(message: Message):
    await message.reply("індекс: 08148")


@router.message(F.text.lower().regexp(lighting_ukr))
async def say_current_status(message: Message):
    if message.chat.type in ('group', 'supergroup'):
        answers = ('Запитай те саме у мене в особистих повідомленнях і я підкажу ;)',
                   "Я можу повідомляти коли з'являється чи зникає світло в вашому будинку",
                   "Почекаємо поки добрі люди підкажуть",
                   "Може є, а може ні. 50/50")

        await message.reply(choice(answers))
    elif message.chat.type == 'private':
        text = await ps.get_current_zones_status()
        await message.answer(text=text)


@router.message(F.text.lower().regexp(lighting_ru))
async def say_current_status_rus(message: Message):
    answers = ("Я знаю, проте не скажу! 🤓", "🤪 расєянську не разумєю",
               "Запитай мене солов'їною 😍", "Зроблю вигляд, що я цього не помітив")
    await message.reply(text=choice(answers))


@router.message(Command(commands=['current_status']))
async def cmd_current_status(message: Message):
    await message.delete()
    if message.chat.type == 'private':
        text = await ps.get_current_zones_status()
        await message.answer(text)
