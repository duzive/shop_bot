import time
from functions.format_number import fn
from functions.low_level.thread import thread
from functions.send_msg import send_msg
from models.conf import Conf
from models.user import User
from config.states import vkcoin, qiwi


@thread
def timer():
    try:
        while True:
            for user in User.objects():
                if user.bonus > 0:
                    user.bonus -= 1
                    user.save()
                    if user.bonus <= 0:
                        send_msg(user.vkid, "💰Вы снова можете получить бонус!")

                user.total_sell_coins[1][1] -= 1
                user.total_sell_coins[1][0] -= 1

                if user.total_sell_coins[1][1] <= 0:
                    user.total_sell_coins[0][0] = 0
                    user.total_sell_coins[1][1] = 24 * 60

                if user.total_sell_coins[1][0] <= 0:
                    user.total_sell_coins[0][1] = 0
                    user.total_sell_coins[1][0] = 24 * 7 * 60

                user.total_buy_coins[1][1] -= 1
                user.total_buy_coins[1][0] -= 1

                if user.total_buy_coins[1][1] <= 0:
                    user.total_buy_coins[0][0] = 0
                    user.total_buy_coins[1][1] = 24 * 60

                if user.total_buy_coins[1][0] <= 0:
                    user.total_buy_coins[0][1] = 0
                    user.total_buy_coins[1][0] = 24 * 7 * 60

                user.total_sell_coins_top_timed -= 1

                if user.total_sell_coins_top_timed <= 0:
                    user.total_sell_coins_top = 0
                    user.total_sell_coins_top_timed = 24 * 7 * 60

                user.total_buy_coins_top_timed -= 1

                if user.total_buy_coins_top_timed <= 0:
                    user.total_buy_coins_top = 0
                    user.total_buy_coins_top_timed = 24 * 7 * 60

                user.save()
            time.sleep(60)

    except Exception as e:
        print(e)
        return timer()


@thread
def vkcoin_handler():
    print("start VKCoin Handler")

    @vkcoin.payment_handler(handler_type="longpoll")
    def handler(data):
        try:
            user = User.get_data(data["from_id"])
            if user.state == "wait_to_get_coins":
                amount = int(data["amount"]) / 1000
                conf = Conf.objects.get(id=1)

                user.total_sell_coins[0][0] += amount
                user.total_sell_coins[0][1] += amount
                user.total_sell_coins[0][2] += amount
                user.total_sell_coins_top += amount
                user.save()

                if user.referer is not None:
                    try:
                        referer = User.get_data(user.referer)
                        referer.total_refs_profit += amount / 100 * 2
                        referer.save()
                        vkcoin.send_payment(referer.vkid, amount / 100 * 2 * 1000, True)
                    except Exception:
                        pass

                conf.total_sells += 1
                conf.total_cap += amount
                conf.last_deals.append(
                    f"💰[id{user.vkid}|{user.f_name}] продал {fn(amount)} VKCoin"
                )
                conf.save()

                qiwi.send(
                    pid=99,
                    recipient=user.qiwi,
                    amount=user.amount_to_pay,
                    comment=f"✅Выплата от WoW Market: №{fn(conf.total_sells)}\n\nСпасибо что вы с нами!",
                )
                send_msg(user.vkid, sticker_id=58254)
                send_msg(
                    user.vkid,
                    "✅Отлично, вы успешно продали мне ваши коины, а я уже отправил деньги на ваш баланс!",
                )

        except Exception as e:
            print(e)
            return vkcoin_handler()

    vkcoin.run_longpoll(tx=[1])
