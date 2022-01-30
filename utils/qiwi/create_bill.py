from random import randint
from config.states import qiwip2p
from models.user import User


def create_bill(user_id, sum, coins):
    try:
        bill_id = randint(1, 123456789)
        lifetime = 30  # Время жизни формы
        comment = "Оплата WoW Market | VKCoin"  # Комментарий
        bill = qiwip2p.bill(
            bill_id=bill_id, amount=sum, lifetime=lifetime, comment=comment
        )  # Выставление счета

        user = User.get_data(user_id)
        user.bill_id = bill_id
        user.bill_coins = coins
        user.save()

        return bill.pay_url
    except:
        return None
