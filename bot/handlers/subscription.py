from typing import Optional

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from ping_app.subscription_service import SubscriptionService


router = Router()

ss = SubscriptionService()


class MySubscription(CallbackData, prefix="my_sub"):
    action: str
    value: Optional[int]


def get_subscription_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Перші лінії", callback_data=MySubscription(action="subscribe", value=1).pack())
    builder.button(text="ЛУ, Соборна", callback_data=MySubscription(action="subscribe", value=2).pack())
    builder.button(text="Відписатись", callback_data=MySubscription(action="unsubscribe").pack())
    builder.adjust(2)

    return builder.as_markup()


@router.message(Command(commands=['subscribe']))
async def check_subscription(message: Message):
    if message.chat.type == 'private':
        user = ss.get_user(user_id=message.from_user.id,
                           full_name=message.from_user.full_name,
                           nickname=message.from_user.username or 'empty')
        text = "У вас немає жодної підписки"

        if user.subscriptions:
            subscriptions_list = [z.zone_group.name for z in user.subscriptions]
            text = f"Ви підписані на: {', '.join(subscriptions_list)}"

        text += "\nОберіть зону, по якій хотіли би отримувати повідомлення"
        await message.answer(text, reply_markup=get_subscription_keyboard())

    elif message.chat.type in ('group', 'supergroup'):
        await message.delete()

        # user = message.from_user
        # answers = ("давай не будемо на людях, перейдемо в особисті\?",
        #            "зараз у мене черга, можу прийняти через 2\-3 тижні, пів-року максимум\.",
        #            "а ви добре себе поводили в цьому році\?")
        # text = f"[{user.full_name}](tg://user?id={user.id}), {random.choice(answers)}"
        # await message.answer(text=text, parse_mode='MarkdownV2')


@router.callback_query(MySubscription.filter(F.action == 'subscribe'))
async def subscribe_zone(query: CallbackQuery, callback_data: MySubscription):
    ss.add_subscription(user_id=query.from_user.id, zone_id=callback_data.value)
    answer = f"Ви підписались на сповіщення по зоні №{callback_data.value}. " \
             f"Я спробую повідомити, коли в ній з'явиться чи зникне електроенергія"
    logger.bind(event=True).info(f"user {query.from_user.id} subscribed to zone #{callback_data.value}")
    await query.message.answer(text=answer)
    await query.answer()


@router.callback_query(MySubscription.filter(F.action == 'unsubscribe'))
async def unsubscribe(query: CallbackQuery):
    ss.delete_all_user_subscriptions(user_id=query.from_user.id)
    logger.bind(event=True).info(f"user {query.from_user.id} unsubscribed :(")
    answer = f"І не дзвони мені більше, і не пиши!"
    await query.message.answer(text=answer)
    await query.answer()
