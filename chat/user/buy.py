from functions.format_number import fn
from config.states import vkcoin
from functions.send_msg import send_msg
from config.states import keyboard
from models.conf import Conf


def buy(user_id):
    conf = Conf.objects.get(id=1)
    if conf.buy_off:
        send_msg(
            user_id,
            "💬Желаете купить коины? Не проблема!\n\n"
            f"👑Наш курс: {conf.buy_price}₽ за 1 000 000 VKCoin"
            f"\n💳Можем продать: {fn(vkcoin.get_balance([282952551])['282952551']/1000)} VKCoin",
            keyboard=keyboard.buy,
        )
    else:
        send_msg(
            user_id,
            "💬Временно не продаем коины, подождите немного...\n\n😥Приносим извинения",
        )
