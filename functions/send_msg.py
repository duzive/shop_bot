from config.states import vk


def send_msg(
    peer_id,
    message: object = None,
    attachment: object = None,
    keyboard: object = None,
    sticker_id: object = None,
):
    try:
        return vk.messages_send(
            peer_id=peer_id,
            message=message,
            attachment=attachment,
            keyboard=keyboard,
            sticker_id=sticker_id,
        )
    except Exception:
        pass
