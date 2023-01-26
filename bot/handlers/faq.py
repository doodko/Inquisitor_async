from random import choice, randint

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from ping_app.ping_service import PingService


router = Router()
ps = PingService()


regexp_base = r".*((дайте)|.*(ка[жз])|(пиш)|(какой)|(який)).*"
ohorona = regexp_base + r"((телефон)|(номер)).*(ох[о]?р[оа]н[иы])"
service_company = regexp_base + r"((телефон)|(номер)).*((ж[єкеэ][хк])|(комфорт.серв[иі]с))"
post_index = regexp_base + r"([іи]ндекс)"
lighting_ukr = r".*((\bсвітло\b.*\bє\b).*|.*(\bє\b.*\bсвітло\b)).*\?"
lighting_ru = r".*((\bсвет\b.*\bесть\b).*|.*(\bесть\b.*\bсвет\b)).*\?"
forecast = r".*(\bколи\b|\bкогда\b).*(буде|дадут|включат|явит[ь]?ся).*(світло|свет).*\?"


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
                   "Я можу повідомляти коли з'являється чи зникає світло у вашій лінії",
                   "Почекаємо поки добрі люди підкажуть",
                   "Може є, а може ні. 50/50",
                   "Підписка на сповіщення безкоштовна. Сусідські нерви - безцінні!")

        await message.reply(choice(answers))
    elif message.chat.type == 'private':
        log = f"current status ukr | {message.from_user.full_name}: {message.text}"
        logger.bind(private=True).info(log)
        text = await ps.get_current_zones_status()
        await message.answer(text=text)


@router.message(F.text.lower().regexp(lighting_ru))
async def say_current_status_rus(message: Message):
    log = f"current status rus | {message.from_user.full_name}: {message.text}"
    logger.bind(private=True).info(log)

    answers = ("Я знаю, проте не скажу! 🤓", "🤪 расєянську не разумєю",
               "Запитай мене солов'їною 😍", "Зроблю вигляд, що я цього не помітив")
    await message.reply(text=choice(answers))


@router.message(Command(commands=['current_status']))
async def cmd_current_status(message: Message):
    await message.delete()
    if message.chat.type == 'private':
        text = await ps.get_current_zones_status()
        await message.answer(text)


@router.message(F.text.lower().regexp(forecast))
async def say_forecast(message: Message):
    log = f"forecast func | {message.from_user.full_name}: {message.text}"
    logger.bind(private=True).info(log)

    answers = ("Треба ще почекати", "Гадаю, вже зовсім скоро!", "А хіба зараз немає? У мене є!",
               "Ой, мабуть не скоро...", "Сьогодні можна і не чекати", "Колись точно буде!",
               "Приблизно через півтори години", "Пішли глянемо у вікно, може у сусідів є?",
               "То тіки впливова жіночка знає", "Світло всередині нас", "Скоро.. Через 2-3 тижні максимум!",
               f"Через {randint(1, 5)} год. {randint(15, 59)} хв. Якщо не буде, то треба дзвонити в ДТЕК!")

    await message.reply(text=choice(answers))
