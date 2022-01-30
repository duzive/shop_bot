from config.states import keyboard
from functions.send_msg import send_msg


def menu(user_id):
    send_msg(user_id, "📝Главное меню", keyboard=keyboard.menu)
