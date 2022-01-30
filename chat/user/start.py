from chat.user.menu import menu
from models.user import User
from functions.send_msg import send_msg
from config.states import vk


def start_bot(event):
    if not User.objects(vkid=event.message.peer_id):
        user = vk.users_get(user_ids=[event.message.peer_id])[0]
        try:
            ref_id = event.message.ref
            referer = User.objects.get(vkid=event.message.ref)
            referer.total_refs += 1
            if referer.push:
                send_msg(
                    referer.vkid,
                    f"[id{event.message.peer_id}|{user['first_name']}] - ваш новый реферал!",
                )
            referer.save()

        except KeyError:
            ref_id = None

        user = User(
            uid=User.get_id(),
            vkid=event.message.peer_id,
            f_name=user["first_name"],
            l_name=user["last_name"],
            referer=ref_id,
        )

        user.total_buy_coins.append([])
        user.total_buy_coins[0].append(0)
        user.total_buy_coins[0].append(0)
        user.total_buy_coins[0].append(0)

        user.total_buy_coins.append([])
        user.total_buy_coins[1].append(0)
        user.total_buy_coins[1].append(0)

        user.total_sell_coins.append([])
        user.total_sell_coins[0].append(0)
        user.total_sell_coins[0].append(0)
        user.total_sell_coins[0].append(0)

        user.total_sell_coins.append([])
        user.total_sell_coins[1].append(0)
        user.total_sell_coins[1].append(0)

        user.save()

        send_msg(user.vkid, sticker_id=13046)
        menu(user.vkid)
