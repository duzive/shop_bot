from random import random
from config.states import vkcoin
from functions.format_number import fn
from functions.send_msg import send_msg
from models.user import User


def bonus(user_id):
    user = User.get_data(user_id)
    if user.total_buy_coins[0][1] >= 1000000:
        if user.bonus <= 0:
            bonus = random.randint(
                int(user.total_buy_coins[0][1] / 1000),
                int(user.total_buy_coins[0][1] / 100),
            )
            user.bonus = 24 * 60
            user.save()
            vkcoin.send_payment(user_id, bonus * 1000, True)
            send_msg(
                user_id,
                f"✅Выпал бонус - {fn(bonus)} VKCoin, и он уже на вашем балансе!\n\n💰Ваш баланс: {fn(vkcoin.get_balance([user_id])[f'{user_id}']/1000)} VKCoin",
            )
        else:
            send_msg(
                user_id, "⛔Вы уже получали бонус за последние 24 часа. Имейте терпение"
            )
    else:
        send_msg(
            user_id, "⛔Чтобы получать бонусы, нужно купить более 1кк VKCoin за неделю"
        )
