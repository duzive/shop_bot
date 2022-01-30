from functions.low_level.thread import thread
from functions.send_msg import send_msg
from functions.match_word import match_word
from models.user import User


@thread
def send_news(user_id, text):
    users = User.objects(news=True)
    num = 0
    send_msg(user_id, "Начинаю рассылку...")
    for user in users:
        try:
            send_msg(user.vkid, text)
            num += 1
        except Exception as e:
            send_msg(user_id, f"⛔Во время отправки рассылки произошла ошибка: {e}")

    send_msg(
        user_id,
        (
            f"✅Рассылка успешно отправлена, её получило {num} {match_word('пользователь', num)}"
            f"\nТекст рассылки:\n\n{text}"
        ),
    )
