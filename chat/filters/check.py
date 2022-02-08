import json
from vk_maria.longpoll.filters import AbstractFilter
from vk_maria import types
from models.user import User


class CheckFilter(AbstractFilter):
    def __init__(self, payload=None, text=None, prefix=None):
        self.payload = payload
        self.text = text
        self.prefix = (".", "/") if prefix is None else prefix

    def have_any_args(self, text):
        try:
            text = text.split(" ")
            if text[0][1:] == self.text:
                if text[1] is not None:
                    return True
            return False

        except Exception:
            return False

    def have_any_word(self, text):
        if type(self.text) == str:
            return any([text[1:] == self.text, text == self.text])
        elif self.text is None:
            return False

        else:
            for word in self.text:
                if any([word == text[1:], word == text]):
                    return True
            return False

    def check(self, event: types.Message):
        text = event.message.text.lower()
        if self.have_any_word(text):
            true_text = True
        else:
            true_text = False

        args_text = self.have_any_args(text)

        try:
            payload = json.loads(event.message.payload)
            return any([payload == self.payload, true_text, args_text])
        except KeyError:
            return any([true_text, args_text])
