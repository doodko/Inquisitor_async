from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from bot.settings_reader import config

router = Router()


@router.message(Command(commands=["health_check"]))
async def cmd_health_check(message: Message):
    await message.answer(text="I'm okay!")


@router.message(Command(commands=["ask_me"]))
async def cmd_ask_me(message: Message):
    await message.delete()

    if message.from_user.id in config.admins:
        if message.reply_to_message:
            query = "одним словом"
            splited_command = message.text.split()
            command = splited_command[0]

            if len(splited_command) > 1:
                query = message.text.replace(command, "").strip()

            answer = f"""
Спробуйте запитати у мене в приватних повідомленнях:
1. Відкриваємо чат @pk_moderatorbot
2. Пишемо запит <b>{query}</b>
3. Отримуємо релевантні результати. Профіт!"""

            await message.reply_to_message.reply(text=answer)


@router.message(Command(commands=["read_rules"]))
async def cmd_read_ruled(message: Message):
    await message.delete()

    if message.from_user.id in config.admins:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
            await message.reply_to_message.delete()

            user_link = f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"
            rules_link = f"<a href='{config.rules_url}'>правилами групи</a>"
            answer = f"{user_link}, ознайомтесь з {rules_link}, будь ласка."

            await message.answer(text=answer)


@router.message(Command(commands=["donate"]))
async def cmd_donate(message: Message):
    if message.chat.type == "private":
        log = f"donate func | {message.from_user.full_name}: {message.text}"
        logger.bind(private=True).info(log)

        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="Підтримати", url=config.jar_url))

        answer = "Подобається сервіс? Ви можете подякувати та підтримати розробника монетою 💰"
        await message.answer(text=answer, parse_mode="MarkdownV2")

    else:
        await message.delete()


@router.message(Command(commands=["start", "help"]))
async def cmd_help(message: Message):
    if message.chat.type == "private":
        answer = f"Коротко запитайте що вас цікавить і я спробую знайти варіанти серед закладів ПК. Я вмію шукати по назві чи ключовим словам.\n\nЗнайшли помилку? <a href='tg://user?id={config.superuser_id}'>Пишіть.</a>"
        await message.answer(text=answer)
    else:
        await message.delete()
