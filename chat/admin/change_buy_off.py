from functions.send_msg import send_msg
from models.conf import Conf


def change_buy_off(admin_id):
    conf = Conf.objects.get(id=1)
    if conf.buy_off:
        conf.buy_off = False
    else:
        conf.buy_off = True
    conf.save()
    send_msg(admin_id, f"Параметр продажи коинов изменен на {conf.buy_off}")
