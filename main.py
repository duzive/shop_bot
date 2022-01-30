from vk_maria import types

from chat.filters.register import RegisterFilter
from chat.filters.check import CheckFilter
from chat.fms.admin_selector import cmd_start
from chat.fms.input_buy_sum import *
from chat.fms.input_qiwi import *
from chat.fms.input_sell_sum import *
from chat.user.bonus import bonus
from chat.user.buy import buy
from chat.user.menu import menu
from chat.user.profile import profile
from chat.user.ref_system import ref_system
from chat.user.sell import sell
from chat.user.start import start_bot
from chat.user.stats import stats
from config.states import lp
from functions.timer import timer, vkcoin_handler
from utils.qiwi.check_bill import check_bill
from utils.users_top import get_users_top


@lp.message_handler(
    CheckFilter({"menu": "back"}, ["меню", "начать", "start"]), RegisterFilter()
)
def menu_handler(event: types.Message):
    menu(event.message.peer_id)


@lp.message_handler(CheckFilter({"menu": "sell"}, "продать"), RegisterFilter())
def coins_sell_handler(event: types.Message):
    sell(event.message.peer_id)


@lp.message_handler(CheckFilter({"menu": "buy"}, "купить"), RegisterFilter())
def coins_buy_handler(event: types.Message):
    buy(event.message.peer_id)


@lp.message_handler(CheckFilter({"menu": "bonus"}, "бонус"), RegisterFilter())
def bonus_hanlder(event: types.Message):
    bonus(event.message.peer_id)


@lp.message_handler(
    CheckFilter({"menu": "ref_sys"}, ["партнерка", "реф", "рефералка"]),
    RegisterFilter(),
)
def ref_hanlder(event: types.Message):
    ref_system(event.message.peer_id)


@lp.message_handler(CheckFilter({"menu": "profile"}, "профиль"), RegisterFilter())
def profile_hanlder(event: types.Message):
    profile(event.message.peer_id)


@lp.message_handler(CheckFilter({"profile": "stats"}, "статистика"), RegisterFilter())
def stats_hanlder(event: types.Message):
    stats(event.message.peer_id)


@lp.message_handler(CheckFilter({"bill": "check"}, "чекбил"), RegisterFilter())
def stats_hanlder(event: types.Message):
    check_bill(event.message.peer_id)


@lp.message_handler(
    CheckFilter({"stats": "top_buyers"}, "топ покупателей"), RegisterFilter()
)
def top_hanlder(event: types.Message):
    top = get_users_top(event.message.peer_id, 1)
    event.reply("👑10 главных покупателей бота за неделю:\n\n" + top)


@lp.message_handler(
    CheckFilter({"stats": "top_sellers"}, "топ продавцов"), RegisterFilter()
)
def top_hanlder(event: types.Message):
    top = get_users_top(event.message.peer_id, 2)
    event.reply("👑10 главных продавцов бота за неделю:\n\n" + top)


@lp.message_handler(CheckFilter({"push": "on"}, "+уведы"), RegisterFilter())
def stats_hanlder(event: types.Message):
    user = User.get_data(event.message.peer_id)
    user.push = True
    user.save()
    event.reply("Вы успешно включили уведомления о новых рефералах")
    ref_system(event.message.peer_id)


@lp.message_handler(CheckFilter({"push": "off"}, "-уведы"), RegisterFilter())
def stats_hanlder(event: types.Message):
    user = User.get_data(event.message.peer_id)
    user.push = False
    user.save()
    event.reply("Вы успешно отключили уведомления о новых рефералах")
    ref_system(event.message.peer_id)


@lp.message_handler()
def other_functions(event: types.Message):
    if "?" in event.message.text:
        cmd_start(event)
    else:
        start_bot(event)


print("bot was started")
try:
    vkcoin_handler()
    timer()
    lp.polling()
except Exception as e:
    print(e)
