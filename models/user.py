from mongoengine import Document
from mongoengine.fields import (
    BooleanField,
    IntField,
    ListField,
    StringField,
    FloatField,
)


class User(Document):
    uid = IntField()
    vkid = IntField()
    f_name = StringField()
    l_name = StringField()

    total_sell_coins = ListField(
        ListField(IntField(default=0))
    )  # [0] => Всего продано за сегодня [0], за неделю [1], за все время [2] /// [1] => Время смерти недельного [0], время смерти сегодняшнего [1]
    total_buy_coins = ListField(
        ListField(IntField(default=0))
    )  # [0] => Всего куплено за сегодня [0], за неделю [1], за все время [2] /// [1] => Время смерти недельного [0], время смерти сегодняшнего [1]

    total_buy_coins_top = IntField(default=0) # Всего куплено для топа
    total_sell_coins_top = IntField(default=0) # Всего продано для топа

    total_buy_coins_top_timed = IntField(default=0)
    total_sell_coins_top_timed = IntField(default=0)

    referer = IntField(null=True)
    total_refs = IntField(default=0)
    total_refs_profit = IntField(default=0)

    news = BooleanField(default=True)
    push = BooleanField(default=True)  # реферальные уведомления
    bonus = IntField(default=0)
    state = StringField(null=True)

    qiwi = IntField(null=True)
    amount_to_pay = FloatField(default=0)
    bill_id = IntField(null=True)  # ID оплаты QIWI
    bill_coins = IntField(null=True)  # Кол-во VKCoin, получаемых после оплаты

    @staticmethod
    def get_data(vk_id=None, user_id=None):
        try:
            if user_id is None:
                user = User.objects.get(vkid=vk_id)
            else:
                user = User.objects.get(uid=user_id)

            return user
        except:
            return None

    @staticmethod
    def get_id():
        return User.objects().count() + 1
