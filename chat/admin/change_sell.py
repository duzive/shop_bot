from functions.send_msg import send_msg
from models.conf import Conf


def change_sell(admin_id, price):
    conf = Conf.objects.get(id=1)
    conf.sell_price = price
    conf.save()
    send_msg(admin_id, f"Новая стоимость покупки 1 000 000 VKCoin = {conf.sell_price}")
