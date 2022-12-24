from typing import Optional

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ping_app.subscription_service import SubscriptionService


router = Router()
router.message.filter(F.chat.type.in_('private'))
ss = SubscriptionService()


class MySubscription(CallbackData, prefix="my_sub"):
    action: str
    value: Optional[int]


def get_subscription_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Перші лінії", callback_data=MySubscription(action="subscribe", value=1).pack())
    builder.button(text="Лу, Соборна", callback_data=MySubscription(action="subscribe", value=2).pack())
    builder.button(text="Відписатись", callback_data=MySubscription(action="unsubscribe").pack())
    builder.adjust(2)

    return builder.as_markup()


@router.message(Command(commands=['subscribe']))
async def check_subscription(message: Message):
    user = ss.get_user(user_id=message.from_user.id,
                       full_name=message.from_user.full_name,
                       nickname=message.from_user.username)
    text = "У вас немає жодної підписки"

    if user.subscriptions:
        subscriptions_list = [z.zone_group.name for z in user.subscriptions]
        text = f"Ви підписані на: {', '.join(subscriptions_list)}"

    text += "\nОберіть зону, по якій хотіли би отримувати повідомлення"
    await message.answer(text, reply_markup=get_subscription_keyboard())


@router.callback_query(MySubscription.filter(F.action == 'subscribe'))
async def subscribe_zone(query: CallbackQuery, callback_data: MySubscription):
    ss.add_subscription(user_id=query.from_user.id, zone_id=callback_data.value)
    answer = f"Ви підписались на сповіщення по зоні №{callback_data.value}. " \
             f"Я спробую повідомити, коли в ній з'явиться чи зникне електроенергія"

    await query.message.answer(text=answer)


@router.callback_query(MySubscription.filter(F.action == 'unsubscribe'))
async def unsubscribe(query: CallbackQuery):
    ss.delete_all_user_subscriptions(user_id=query.from_user.id)
    answer = f"І не дзвони мені більше і не пиши!"
    await query.message.answer(text=answer)