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


class InputSellSum(StatesGroup):
    input_sell_sum: State


@lp.message_handler(
    CheckFilter({"sell": "sell"}),
    RegisterFilter(),
)
def process_sum(event: types.Message):
    try:
        InputSellSum.input_sell_sum.set()
        event.reply(
            f"📝Введите количество VKCoin, которое желаете продать нам\n\n💰Ваш баланс: {fn(vkcoin.get_balance([event.message.peer_id])[f'{event.message.peer_id}']/1000)} VKCoin",
            keyboard=keyboard.back,
        )
    except Exception as e:
        event.reply(
            f"Проверьте свой VKCoin кошелек. Он шлет ошибку, более подробно: \n\n{e}"
        )


@lp.message_handler(state=InputSellSum.input_sell_sum)
def process_final(event: types.Message):
    if event.message.text.lower() != "назад":
        if check_input(event.message.peer_id, event.message.text):
            user = User.get_data(event.message.peer_id)
            money = (
                int(event.message.text) / 1000000 * Conf.objects.get(id=1).sell_price
            )
            if money >= 1:
                if qiwi.balance() >= money:
                    if vkcoin.get_balance([event.message.peer_id])[
                        f"{event.message.peer_id}"
                    ] / 1000 >= int(event.message.text):
                        user.state = "wait_to_get_coins"
                        user.amount_to_pay = money
                        user.save()
                        link = vkcoin.get_payment_url(
                            int(event.message.text) * 1000, free_amount=False
                        )
                        send_msg(
                            user.vkid,
                            f"✅Отлично! Я сформировал ссылку для перевода VKCoin\n\n👉🏻 {link}\n💰Вы получите денежное вознаграждение {te(money, 2)}₽ на QIWI (+{user.qiwi}) в течение нескольких минут",
                        )
                        menu(user.vkid)
                        InputSellSum.finish()
                    else:
                        send_msg(
                            user.vkid,
                            "⛔На вашем счете нет столько VKCoin. Поговорим, когда они появятся",
                        )
                else:
                    send_msg(
                        user.vkid,
                        "⛔Вы хотите продать больше, чем мы можем себе позволить :("
                        "\n⏱Стоит немного изменить сумму продажи, или попробовать позже...",
                    )
            else:
                send_msg(
                    user.vkid,
                    "⛔При продаже такого количества VKCoin, вы получите меньше рубля. Это слишном мало"
                    "\n💰Стоит немного увеличить сумму продажи...",
                )
    else:
        InputSellSum.finish()
        menu(event.message.peer_id)
