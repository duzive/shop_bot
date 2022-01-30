from vk_maria.longpoll.filters import AbstractFilter
from vk_maria import types
from models.user import User


class RegisterFilter(AbstractFilter):
    def check(self, event: types.Message):
        return User.objects(vkid=event.message.peer_id)
