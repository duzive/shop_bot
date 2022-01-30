from functions.send_msg import send_msg
from models.conf import Conf


def change_sell_off(admin_id):
    conf = Conf.objects.get(id=1)
    if conf.sell_off:
        conf.sell_off = False
    else:
        conf.sell_off = True
    conf.save()
    send_msg(admin_id, f"Параметр покупки коинов изменен на {conf.sell_off}")
