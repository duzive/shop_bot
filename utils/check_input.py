from functions.send_msg import send_msg


def check_input(user, text, rules=None):
    try:
        int(text)
    except ValueError:
        send_msg(user, "⛔Только цифры. Я не люблю текст. Цифры.")
        return False

    if int(text) > 0:
        if rules is None:
            return True
        else:
            if rules == "qiwi":
                if len(text) < 10 or len(text) > 15 or "+" in text:
                    send_msg(user, "⛔Что-то не похоже на номер QIWI. Проверьте ввод")
                    return False
                else:
                    return True
    else:
        send_msg(user, "⛔Только цифры больше нуля. Больше нуля.")
        return False
