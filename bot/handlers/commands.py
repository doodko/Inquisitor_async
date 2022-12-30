from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ping_app.periods_service import PeriodService
from settings_reader import config


router = Router()
ps = PeriodService()


@router.message(Command(commands=['health_check']))
async def cmd_health_check(message: Message):
    await message.answer(text="I'm okay!")


@router.message(Command(commands=['ask_volodya']))
async def cmd_ask_volodya(message: Message):
    await message.delete()

    if message.from_user.id in config.admins:
        if message.reply_to_message:
            query = 'одним словом'
            command = message.text.split()[0]

            if len(message.text.split()) > 1:
                query = message.text.replace(command, "").strip()

            answer = f"""
            Спробуйте запитати у Володі:
            1. Відкриваємо чат з ботом @pkvartal_bot
            2. Пишемо йому запит <b>{query}</b>
            3. Отримуємо релевантні результати. Профіт!"""

            await message.reply_to_message.reply(text=answer)


@router.message(Command(commands=['read_rules']))
async def cmd_read_ruled(message: Message):
    await message.delete()

    if message.from_user.id in config.admins:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
            await message.reply_to_message.delete()

            rules_url = 'https://telegra.ph/Pravila-grupi-Petr%D1%96vskij-kvartal-10-20'
            answer = f"[{user.full_name}](tg://user?id={user.id}), ознайомтесь з " \
                     f"[правилами групи]({rules_url}), будь ласка\."

            await message.answer(text=answer, parse_mode='MarkdownV2')


@router.message(Command(commands=['stats']))
async def cmd_stats(message: Message):
    start, end = ps.get_date_period_from_message(message.text)
    if start > end:
        start, end = end, start
    text = f"Статистика за період з <b>{start.date()}</b> по <b>{end.date()}</b>"
    if start == end:
        text = f"Статистика за <b>{start.date()}</b>"
    if start.date() >= datetime.today().date() or end.date() >= datetime.today().date():
        text = "Зараз дістану кришталеву і загляну в майбутнє"

    await message.answer(text=text)


@router.message(Command(commands=['donate']))
async def cmd_donate(message: Message):
    text = "Подобається сервіс\? Ви можете [підтримати розробника](https://send.monobank.ua/jar/CXDBhb4LV) монетою"

    if message.chat.type in ('group', 'supergroup'):
        await message.delete()
    if message.chat.type == 'private':
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="Підтримати", url="https://send.monobank.ua/jar/CXDBhb4LV"))

        await message.answer('Подобається сервіс? Ви можете подякувати та підтримати розробника монетою 💰',
                             reply_markup=builder.as_markup())
