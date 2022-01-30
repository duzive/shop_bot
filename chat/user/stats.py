from functions.format_number import fn
from functions.send_msg import send_msg
from models.conf import Conf
from config.states import keyboard


def stats(user_id):
    conf = Conf.objects.get(id=1)
    deals = "\n".join(conf.last_deals[-5:])
    send_msg(
        user_id,
        f"👥Общая статистика пользователей:\n\n"
        f"💳Всего покупок: {fn(conf.total_buys)}\n"
        f"💰Всего продаж: {fn(conf.total_sells)}\n"
        f"📈Общий оборот: {fn(conf.total_cap)} VKCoin\n\n"
        f"💼Последние сделки:\n{deals}",
        keyboard=keyboard.stats,
    )
