from aiogram import Router, F
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message

from ping_app.ping_service import PingService

router = Router()
ps = PingService()


regexp_base = r".*((дайте)|.*(ка[жз])|(пиш)|(какой)|(який)).*"
ohorona = regexp_base + r"((телефон)|(номер)).*(ох[о]?р[оа]н[иы])"
service_company = regexp_base + r"((телефон)|(номер)).*((ж[єкеэ][хк])|(комфорт.серв[иі]с))"
post_index = regexp_base + r"([іи]ндекс)"

kivi = r".*\b(кав[ауио]|кофе|ф[иі]льтр|[эе]спре[с]+о|капуч[іи]но|латте|п[иі][ц]+а|сендв[иі]ч|бургер|сніданок|завтрак|" \
       r"тістечка|круасан|смаколик|торт|макар[оу]н|кафе|ресторан|кав\'ярн|п[иі][ц]+ер[иі])"


@router.message(F.text.lower().regexp(ohorona))
async def say_security_service_phone(message: Message):
    await message.reply("+380674092276")


@router.message(F.text.lower().regexp(service_company))
async def say_service_company_phone(message: Message):
    await message.reply("+380672247713\n+380670000012 (цілодобовий)")


@router.message(F.text.lower().regexp(post_index))
async def say_index(message: Message):
    await message.reply("індекс: 08148")


@router.message(F.text.lower().regexp(kivi))
async def ping_kivi(message: Message):
    try:
        await message.forward(chat_id=798798016)
    except TelegramForbiddenError:
        pass
