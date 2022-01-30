from mongoengine import Document
from mongoengine.fields import (
    IntField,
    ListField,
    StringField,
    BooleanField,
    FloatField,
)


class Conf(Document):
    id = IntField(primary_key=True)

    sell_price = FloatField(default=5)
    buy_price = FloatField(default=6)

    buy_off = BooleanField(default=True)
    sell_off = BooleanField(default=True)

    total_sells = IntField(default=0)
    total_buys = IntField(default=0)

    total_cap = IntField(default=0)  # Общее число продаж в коинах за все время

    last_deals = ListField(StringField(null=True))
