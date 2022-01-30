from functions.format_number import fn
from models.user import User
from functions.match_word import match_word


def get_users_top(user_id, view=1):
    top = ""
    user_in_top = ""
    rows = (
        User.objects()
        .order_by("-total_buy_coins_top" if view == 1 else "-total_sell_coins_top")
        .limit(10)
    )

    for num, row in enumerate(rows, 1):
        top += f"{num}. [id{row.vkid}|{row.f_name} {row.l_name}] - {fn(row.total_buy_coins_top) if view == 1 else fn(row.total_sell_coins_top)} VKCoin\n"
        user_in_top += f"{row.vkid} "

    if user_id < 2000000000:
        if str(user_id) not in user_in_top:
            rows = User.objects().order_by("-dick")
            for num, row in enumerate(rows, 1):
                if row.vkid == user_id:
                    top += "〰" * 7
                    top += f"\n{num}. [id{user_id}|Вы] - {fn(row.total_buy_coins_top) if view == 1 else fn(row.total_sell_coins_top)} VKCoin"
                    break

    return top
