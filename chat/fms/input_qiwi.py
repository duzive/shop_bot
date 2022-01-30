from vk_maria.longpoll.fsm import StatesGroup, State
from vk_maria import types
from chat.user.menu import menu
from functions.send_msg import send_msg
from models.conf import Conf
from models.user import User
from config.states import lp, keyboard, vkcoin, qiwi
from chat.filters.register import RegisterFilter
from chat.filters.check import CheckFilter
from utils.check_input import check_input
from utils.qiwi.create_bill import create_bill


class InputQiwi(StatesGroup):
    number: State


@lp.message_handler(
    CheckFilter({"sell": "qiwi"}, "qiwi"),
    RegisterFilter(),
)
def process_sum(event: types.Message):
    InputQiwi.number.set()
    event.reply(
        "📝Введите номер нового Qiwi кошелька, без +",
        keyboard=keyboard.back,
    )


@lp.message_handler(state=InputQiwi.number)
def process_final(event: types.Message):
    if event.message.text.lower() != "назад":
        if check_input(event.message.peer_id, event.message.text, rules="qiwi"):
            user = User.get_data(event.message.peer_id)
            user.qiwi = event.message.text
            user.save()
            send_msg(
                event.message.peer_id,
                f"💰Ваш Qiwi для выплат успешно изменен на +{user.qiwi}",
            )
            InputQiwi.finish()
            menu(event.message.peer_id)

    else:
        InputQiwi.finish()
        menu(event.message.peer_id)
