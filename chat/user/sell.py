from functions.format_number import fn
from functions.send_msg import send_msg
from config.states import qiwi, keyboard
from models.conf import Conf
from models.user import User


def sell(user_id):
    conf = Conf.objects.get(id=1)
    user = User.get_data(user_id)
    if conf.sell_off:
        if user.qiwi is not None:
            send_msg(
                user_id,
                f"💬Купите мои коины?.. Еще спрашиваете?!\n\n"
                f"👑Наш курс: {conf.sell_price}₽ за 1 000 000 VKCoin"
                f"\n💰Можем купить: {fn(qiwi.balance() / conf.sell_price * 1000000)} VKCoin",
                keyboard=keyboard.sell,
            )
        else:
            send_msg(
                user_id,
                "⛔У вас не установлен QIWI-счет для получения выплат, используйте команду /qiwi\n\nПосле установки вы сможете продавать нам ваши коины!",
                keyboard=keyboard.qiwi,
            )
    else:
        send_msg(
            user_id,
            "💬Временно не покупаем коины, подождите немного...\n\n😥Приносим извинения",
        )
