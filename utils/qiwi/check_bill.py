from chat.user.menu import menu
from config.states import qiwip2p, vkcoin
from functions.format_number import fn
from models.conf import Conf
from models.user import User
from functions.send_msg import send_msg


def check_bill(user_id):
    user = User.get_data(user_id)
    bill_status = qiwip2p.check(user.bill_id).status
    if bill_status == "PAID":

        config = Conf.objects.get(id=1)
        config.total_buys += 1
        config.total_cap += user.bill_coins
        config.last_deals.append(
            f"📈[id{user.vkid}|{user.f_name}] купил {fn(user.bill_coins)} VKCoin"
        )
        config.save()

        vkcoin.send_payment(user.vkid, user.bill_coins * 1000, True)

        send_msg(
            user_id,
            f"💎Оплата прошла успешно, спасибо!\n\n💜Я уже отправил вам {fn(user.bill_coins)} VKCoin",
        )
        menu(user_id)

        user.total_buy_coins[0][0] += user.bill_coins
        user.total_buy_coins[0][1] += user.bill_coins
        user.total_buy_coins[0][2] += user.bill_coins
        user.total_buy_coins_top += user.bill_coins

        if user.referer is not None:
            referer = User.get_data(user.referer)
            referer.total_refs_profit += user.bill_coins / 100 * 2
            referer.save()
            vkcoin.send_payment(referer.vkid, user.bill_coins / 100 * 2 * 1000, True)

        user.bill_coins = None
        user.bill_id = None
        user.save()


        return True

    else:
        send_msg(user_id, "⛔Не вижу оплаты. Спросите, когда оплатите")
        return False
