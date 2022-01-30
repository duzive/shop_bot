from vk_maria import Vk
from vk_maria.longpoll.fsm import MemoryStorage
from vk_maria.longpoll import LongPoll
from vk_maria.keyboard import KeyboardAssociator
from config.data import MONGO_HOST, QIWI_TOKEN, QIWIP2P_TOKEN, VK_TOKEN, VKCOIN_TOKEN
import pymorphy2
from pyqiwip2p import QiwiP2P
import pyqiwi
from mongoengine import connect
from vkcoin import VKCoin


vk = Vk(VK_TOKEN)
lp = LongPoll(vk, MemoryStorage())

vkcoin = VKCoin(user_id=282952551, key=VKCOIN_TOKEN)

morph = pymorphy2.MorphAnalyzer()

mongo_connect = connect(host=MONGO_HOST)

qiwip2p = QiwiP2P(auth_key=QIWIP2P_TOKEN)
qiwi = pyqiwi.Wallet(QIWI_TOKEN)

keyboard = KeyboardAssociator(folder="keyboards")
