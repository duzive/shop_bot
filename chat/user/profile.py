from functions.format_number import fn
from functions.match_word import match_word
from functions.send_msg import send_msg
from models.user import User
from config.states import keyboard


def profile(user_id):
    user = User.get_data(user_id)
    send_msg(
        user_id,
        f"👤[id{user_id}|Ваш] профиль:"
        f"\n\n📈Всего куплено:"
        f"\nЗа сегодня: {fn(user.total_buy_coins[0][0])} VK Coin"
        f"\nЗа неделю: {fn(user.total_buy_coins[0][1])} VKCoin"
        f"\nЗа все время: {fn(user.total_buy_coins[0][2])} VKCoin"
        f"\n\n📉Всего продано:"
        f"\nЗа сегодня: {fn(user.total_sell_coins[0][0])} VKCoin"
        f"\nЗа неделю: {fn(user.total_sell_coins[0][1])} VKCoin"
        f"\nЗа все время: {fn(user.total_sell_coins[0][2])} VKCoin"
        f"\n\n👥Всего рефералов: {fn(user.total_refs)}"
        f"\n💰Рефералы принесли: {fn(user.total_refs_profit)} VKCoin"
        f"\n\n💳QIWI: {user.qiwi if user.qiwi is not None else 'не указан'}"
        f"\n👑Бонус: {'доступен' if user.bonus <= 0 else 'доступен через {} {}'.format(user.bonus/60, match_word('час', int(user.bonus/60)))}"
        f"\n💬Рассылки: {'включены' if user.news else 'отключены'}",
        keyboard=keyboard.profile,
    )
