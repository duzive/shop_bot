from functions.send_msg import send_msg
from models.conf import Conf


def change_buy(admin_id, price):
    conf = Conf.objects.get(id=1)
    conf.buy_price = price
    conf.save()
    send_msg(admin_id, f"Новая стоимость продажи 1 000 000 VKCoin = {conf.buy_price}")
