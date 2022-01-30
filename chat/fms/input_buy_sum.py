from vk_maria.longpoll.fsm import StatesGroup, State
from vk_maria import types
from chat.user.menu import menu
from functions.format_number import fn
from functions.send_msg import send_msg
from functions.truncate import te
from models.conf import Conf
from models.user import User
from config.states import lp, keyboard, vkcoin, qiwi
from chat.filters.register import RegisterFilter
from chat.filters.check import CheckFilter
from utils.check_input import check_input
from utils.qiwi.create_bill import create_bill


class InputBuySum(StatesGroup):
    input_buy_sum: State


@lp.message_handler(
    CheckFilter({"buy": "buy"}),
    RegisterFilter(),
)
def process_sum(event: types.Message):
    try:
        InputBuySum.input_buy_sum.set()
        event.reply(
            "📝Введите количество VKCoin, которое желаете купить",
            keyboard=keyboard.back,
        )
    except Exception as e:
        event.reply(
            f"Проверьте свой VKCoin кошелек. Он шлет ошибку, более подробно: \n\n{e}"
        )


@lp.message_handler(state=InputBuySum.input_buy_sum)
def process_final(event: types.Message):
    if event.message.text.lower() != "назад":
        if check_input(event.message.peer_id, event.message.text):
            user = User.get_data(event.message.peer_id)
            money = int(event.message.text) / 1000000 * Conf.objects.get(id=1).buy_price
            if vkcoin.get_balance([282952551])["282952551"] / 1000 >= int(
                event.message.text
            ):
                if money >= 1:
                    bill = create_bill(user.vkid, money, event.message.text)
                    InputBuySum.finish()
                    if bill is not None:
                        send_msg(
                            user.vkid,
                            f"💜Отлично, я сформировал ссылку для оплаты"
                            f"\n\n💬Оплатить тут: {bill}"
                            f"\n💳Сумма: {te(money, 2)} руб."
                            f"\n💰Вы получите: {fn(event.message.text)} VKCoin",
                            keyboard=keyboard.check_bill,
                        )
                    else:
                        send_msg(
                            user.vkid,
                            "⛔Произошла ошибка на стороне QIWI, повторите попытку оплаты позже :(",
                        )
                        InputBuySum.finish()
                        menu(user.vkid)
                else:
                    send_msg(
                        user.vkid,
                        "⛔Не получится купить VKCoin менее, чем на 1 рубль. Это ограничение Qiwi",
                    )
            else:
                send_msg(
                    user.vkid,
                    "⛔Вы хотите купить больше, чем мы можем продать :("
                    "\n⏱Стоит немного изменить сумму покупки, или попробовать позже...",
                )
    else:
        InputBuySum.finish()
        menu(event.message.peer_id)
