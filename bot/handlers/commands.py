from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.start_bot import bot
from settings_reader import config


router = Router()
router.message.filter(F.from_user.id.in_(config.admins))


# @router.message(Command(commands=['send_message']))
# async def cmd_send_message(message: Message):
#     msg = message.text[13:]
#     await bot.send_message(chat_id='-1001092707720', text=msg)


@router.message(Command(commands=['health_check']))
async def cmd_health_check(message: Message):
    await message.answer(text="I'm okay!")


@router.message(Command(commands=['ask_volodya']))
async def cmd_ask_volodya(message: Message):
    await message.delete()

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

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        await message.reply_to_message.delete()

        rules_url = 'https://telegra.ph/Pravila-grupi-Petr%D1%96vskij-kvartal-10-20'
        answer = f"[{user.full_name}](tg://user?id={user.id}), ознайомтесь з " \
                 f"[правилами групи]({rules_url}), будь ласка\."

        await message.answer(text=answer, parse_mode='MarkdownV2')
