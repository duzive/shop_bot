from vk_maria import types
from chat.admin.change_buy import change_buy
from chat.admin.change_buy_off import change_buy_off
from chat.admin.change_sell import change_sell
from chat.admin.change_sell_off import change_sell_off

from functions.send_msg import send_msg
from functions.send_news import send_news
from models.user import User


def cmd_start(event: types.Message):
    if event.message.peer_id == 282952551:
        try:
            mess = event.message.text.replace("? ", "").split(", ")
            print(mess)

            if mess[0] == "news":
                send_news(event.message.peer_id, mess[1])

            elif mess[0] == "sell":
                change_sell(event.message.peer_id, float(mess[1]))

            elif mess[0] == "buy":
                change_buy(event.message.peer_id, float(mess[1]))

            elif mess[0] == "sell_off":
                change_sell_off(event.message.peer_id)

            elif mess[0] == "buy_off":
                change_buy_off(event.message.peer_id)

        except Exception as e:
            send_msg(event.message.peer_id, f"Неверная команда администратора\n\n{e}")
