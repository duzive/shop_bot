from functions.format_number import fn
from functions.match_word import match_word
from config.states import keyboard
from functions.send_msg import send_msg
from models.user import User


def ref_system(user_id):
    user = User.get_data(user_id)
    send_msg(
        user_id,
        f"👥Приглашайте друзей в нашего бота - получайте 2% с каждой их сделки!\n"
        f"👑Например, пригласив 10 человек, которые купят по 10кк коинов, вы получите 2кк совешенно бесплатно!\n\n"
        f"💬Ваша партнерская ссылка: vk.me/wow_vkc?ref={user_id}\n"
        f"✅Вы пригласили: {fn(user.total_refs)} {match_word('пользователь', user.total_refs)}\n"
        f"💰Рефералы принесли: {fn(user.total_refs_profit)} VKCoin",
        keyboard=keyboard.push_off if user.push else keyboard.push_on,
    )
